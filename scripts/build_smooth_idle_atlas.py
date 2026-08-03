#!/usr/bin/env python3
"""Build and validate Kano's animated atlas for a Codex Pet v2."""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageSequence

ATLAS_WIDTH = 1536
ATLAS_HEIGHT = 2288
CELL_WIDTH = 192
CELL_HEIGHT = 208
IDLE_FRAME_COUNT = 6
FRAME_DURATIONS_MS = (100, 4600, 100, 100, 100, 100)
JUMPING_ROW = 4
WORKING_ROW = 7
GROUND_BOTTOM = 203
TOP_MARGIN = 5
STATE_SCALES = {"working": 0.92, "jumping": 1.15}


class AtlasError(ValueError):
    pass


def _riff_chunks(data: bytes):
    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise AtlasError("output is not a RIFF WebP file")

    offset = 12
    while offset + 8 <= len(data):
        name = data[offset : offset + 4]
        size = int.from_bytes(data[offset + 4 : offset + 8], "little")
        payload_start = offset + 8
        payload_end = payload_start + size
        if payload_end > len(data):
            raise AtlasError(f"truncated WebP chunk {name!r}")
        yield name, data[payload_start:payload_end]
        offset = payload_end + (size & 1)


def _riff_chunk(name: bytes, payload: bytes) -> bytes:
    padding = b"\0" if len(payload) & 1 else b""
    return name + len(payload).to_bytes(4, "little") + payload + padding


def _uint24(value: int) -> bytes:
    return value.to_bytes(3, "little")


def _exact_webp_image_chunks(image: Image.Image) -> bytes:
    encoded = io.BytesIO()
    image.save(
        encoded,
        format="WEBP",
        lossless=True,
        quality=100,
        alpha_quality=100,
        method=6,
        exact=True,
    )
    chunks = [
        _riff_chunk(name, payload)
        for name, payload in _riff_chunks(encoded.getvalue())
        if name in {b"ALPH", b"VP8 ", b"VP8L"}
    ]
    if not chunks:
        raise AtlasError("exact WebP frame has no image data")
    return b"".join(chunks)


def _animation_frame_chunk(image: Image.Image, duration_ms: int) -> bytes:
    width, height = image.size
    header = b"".join(
        (
            _uint24(0),
            _uint24(0),
            _uint24(width - 1),
            _uint24(height - 1),
            _uint24(duration_ms),
            b"\x02",
        )
    )
    return _riff_chunk(b"ANMF", header + _exact_webp_image_chunks(image))


def _save_exact_animation(frames: list[Image.Image], path: Path) -> None:
    if len(frames) != len(FRAME_DURATIONS_MS):
        raise AtlasError(
            f"animation must contain {len(FRAME_DURATIONS_MS)} frames, "
            f"got {len(frames)}"
        )
    vp8x = b"\x12\0\0\0" + _uint24(ATLAS_WIDTH - 1) + _uint24(
        ATLAS_HEIGHT - 1
    )
    anim = b"\0\0\0\0\0\0"
    frame_chunks = [_animation_frame_chunk(frames[0], FRAME_DURATIONS_MS[0])]
    frame_chunks.extend(
        _animation_frame_chunk(
            frame.crop((0, 0, ATLAS_WIDTH, CELL_HEIGHT)),
            FRAME_DURATIONS_MS[phase],
        )
        for phase, frame in enumerate(frames[1:], start=1)
    )
    body = b"WEBP" + _riff_chunk(b"VP8X", vp8x) + _riff_chunk(b"ANIM", anim)
    body += b"".join(frame_chunks)
    path.write_bytes(b"RIFF" + len(body).to_bytes(4, "little") + body)


def inspect_animated_webp(path: Path) -> dict[str, object]:
    animation = False
    loop = None
    durations: list[int] = []
    for name, payload in _riff_chunks(Path(path).read_bytes()):
        if name == b"VP8X":
            if len(payload) < 10:
                raise AtlasError("invalid VP8X chunk")
            animation = bool(payload[0] & 0x02)
        elif name == b"ANIM":
            if len(payload) < 6:
                raise AtlasError("invalid ANIM chunk")
            loop = int.from_bytes(payload[4:6], "little")
        elif name == b"ANMF":
            if len(payload) < 16:
                raise AtlasError("invalid ANMF chunk")
            durations.append(int.from_bytes(payload[12:15], "little"))

    return {
        "animation": animation,
        "loop": loop,
        "durations_ms": durations,
    }


def _difference_bbox(first: Image.Image, second: Image.Image):
    return ImageChops.difference(first, second).getbbox(alpha_only=False)


def _transparent_rgb_residue_count(image: Image.Image) -> int:
    rgba = image.convert("RGBA")
    red, green, blue, alpha = rgba.split()
    rgb_nonzero = ImageChops.lighter(red, ImageChops.lighter(green, blue))
    transparent = alpha.point(lambda value: 255 if value == 0 else 0)
    residue = ImageChops.multiply(rgb_nonzero, transparent)
    return sum(residue.histogram()[1:])


def _load_static_source(source_path: Path) -> Image.Image:
    try:
        with Image.open(source_path) as opened:
            if getattr(opened, "is_animated", False):
                raise AtlasError("source atlas must be static")
            if opened.size != (ATLAS_WIDTH, ATLAS_HEIGHT):
                raise AtlasError(
                    f"source atlas must be {ATLAS_WIDTH}x{ATLAS_HEIGHT}, "
                    f"got {opened.width}x{opened.height}"
                )
            if "A" not in opened.mode:
                raise AtlasError("source atlas must have an alpha channel")
            source = opened.convert("RGBA").copy()
    except AtlasError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise AtlasError(f"could not open source atlas: {exc}") from exc

    residue = _transparent_rgb_residue_count(source)
    if residue:
        raise AtlasError(
            f"source atlas has {residue} transparent pixels with RGB residue"
        )
    return source


def _scale_cell(image: Image.Image, scale: float, state: str) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return image.copy()

    _, _, _, bottom = bbox
    sprite = image.crop(bbox)
    width = round(sprite.width * scale)
    height = round(sprite.height * scale)
    sprite = sprite.resize((width, height), Image.Resampling.LANCZOS)

    x = round(CELL_WIDTH / 2 - width / 2)
    if state == "working":
        y = GROUND_BOTTOM - height
    else:
        y = bottom - height
        y = max(TOP_MARGIN, min(y, GROUND_BOTTOM - height))

    result = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
    result.alpha_composite(sprite, (x, y))
    return result


def _apply_state_scales(source: Image.Image) -> Image.Image:
    scaled = source.copy()
    for row, state in ((WORKING_ROW, "working"), (JUMPING_ROW, "jumping")):
        for column in range(ATLAS_WIDTH // CELL_WIDTH):
            box = (
                column * CELL_WIDTH,
                row * CELL_HEIGHT,
                (column + 1) * CELL_WIDTH,
                (row + 1) * CELL_HEIGHT,
            )
            cell = source.crop(box)
            if cell.getchannel("A").getbbox() is None:
                continue
            scaled.paste(_scale_cell(cell, STATE_SCALES[state], state), box[:2])
    return scaled


def _build_frames(source: Image.Image) -> list[Image.Image]:
    scaled_source = _apply_state_scales(source)
    frames: list[Image.Image] = []
    for phase in range(IDLE_FRAME_COUNT):
        frame = scaled_source.copy()
        idle = source.crop(
            (
                phase * CELL_WIDTH,
                0,
                (phase + 1) * CELL_WIDTH,
                CELL_HEIGHT,
            )
        )
        for column in range(IDLE_FRAME_COUNT):
            frame.paste(idle, (column * CELL_WIDTH, 0))
        frames.append(frame)
    return frames


def _validate_output(path: Path, source: Image.Image) -> dict[str, object]:
    metadata = inspect_animated_webp(path)
    expected_durations = list(FRAME_DURATIONS_MS)
    if not metadata["animation"]:
        raise AtlasError("output WebP is not animated")
    if metadata["loop"] != 0:
        raise AtlasError(f"output loop must be 0, got {metadata['loop']}")
    if metadata["durations_ms"] != expected_durations:
        raise AtlasError(
            f"output durations must be {expected_durations}, "
            f"got {metadata['durations_ms']}"
        )

    expected_static = _apply_state_scales(source)
    for row in range(1, ATLAS_HEIGHT // CELL_HEIGHT):
        if row in {JUMPING_ROW, WORKING_ROW}:
            continue
        box = (0, row * CELL_HEIGHT, ATLAS_WIDTH, (row + 1) * CELL_HEIGHT)
        if _difference_bbox(expected_static.crop(box), source.crop(box)) is not None:
            raise AtlasError(f"state scaling changed non-target row {row}")

    neutral_and_unused = expected_static.crop(
        (IDLE_FRAME_COUNT * CELL_WIDTH, 0, ATLAS_WIDTH, CELL_HEIGHT)
    )
    expected_non_idle = expected_static.crop(
        (0, CELL_HEIGHT, ATLAS_WIDTH, ATLAS_HEIGHT)
    )
    frame_count = 0
    residue_counts: list[int] = []
    try:
        with Image.open(path) as opened:
            if not getattr(opened, "is_animated", False):
                raise AtlasError("decoded output is not animated")
            if opened.n_frames != len(FRAME_DURATIONS_MS):
                raise AtlasError(
                    f"decoded output must have {len(FRAME_DURATIONS_MS)} frames, "
                    f"got {opened.n_frames}"
                )
            for phase, decoded in enumerate(ImageSequence.Iterator(opened)):
                frame = decoded.convert("RGBA")
                if frame.size != (ATLAS_WIDTH, ATLAS_HEIGHT):
                    raise AtlasError(f"decoded phase {phase} has wrong dimensions")
                expected_idle = source.crop(
                    (
                        phase * CELL_WIDTH,
                        0,
                        (phase + 1) * CELL_WIDTH,
                        CELL_HEIGHT,
                    )
                )
                for column in range(IDLE_FRAME_COUNT):
                    actual_idle = frame.crop(
                        (
                            column * CELL_WIDTH,
                            0,
                            (column + 1) * CELL_WIDTH,
                            CELL_HEIGHT,
                        )
                    )
                    if _difference_bbox(actual_idle, expected_idle) is not None:
                        raise AtlasError(
                            f"decoded phase {phase} idle column {column} changed pixels"
                        )
                if _difference_bbox(
                    frame.crop(
                        (IDLE_FRAME_COUNT * CELL_WIDTH, 0, ATLAS_WIDTH, CELL_HEIGHT)
                    ),
                    neutral_and_unused,
                ) is not None:
                    raise AtlasError(
                        f"decoded phase {phase} changed neutral or unused cells"
                    )
                if _difference_bbox(
                    frame.crop((0, CELL_HEIGHT, ATLAS_WIDTH, ATLAS_HEIGHT)),
                    expected_non_idle,
                ) is not None:
                    raise AtlasError(f"decoded phase {phase} changed non-idle rows")
                residue_counts.append(_transparent_rgb_residue_count(frame))
                frame_count += 1
    except AtlasError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise AtlasError(f"could not decode output atlas: {exc}") from exc

    if any(residue_counts):
        raise AtlasError(
            f"decoded output has transparent RGB residue by phase: {residue_counts}"
        )

    return {
        "ok": True,
        "file": str(path.resolve()),
        "format": "WEBP",
        "mode": "RGBA",
        "columns": 8,
        "rows": 11,
        "sprite_version_number": 2,
        "width": ATLAS_WIDTH,
        "height": ATLAS_HEIGHT,
        "frame_count": frame_count,
        "durations_ms": expected_durations,
        "cycle_duration_ms": sum(FRAME_DURATIONS_MS),
        "loop": metadata["loop"],
        "transparent_rgb_residue_pixels": max(residue_counts, default=0),
        "preservation": {
            "idle_phase_mapping": "passed",
            "neutral_and_unused_cells": "pixel-identical",
            "non_target_rows": "pixel-identical",
            "working_scale": STATE_SCALES["working"],
            "jumping_scale": STATE_SCALES["jumping"],
        },
        "errors": [],
        "warnings": [],
    }


def _write_json_atomic(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        temporary.write_text(
            json.dumps(value, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def build_smooth_idle_atlas(
    source_path: Path,
    output_path: Path,
    report_path: Path | None = None,
) -> dict[str, object]:
    source_path = Path(source_path).expanduser().resolve()
    output_path = Path(output_path).expanduser().resolve()
    if report_path is not None:
        report_path = Path(report_path).expanduser().resolve()

    source = _load_static_source(source_path)
    frames = _build_frames(source)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.", suffix=".tmp.webp", dir=output_path.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        _save_exact_animation(frames, temporary)
        del frames
        result = _validate_output(temporary, source)
        result["file"] = str(output_path)
        os.replace(temporary, output_path)
        if report_path is not None:
            _write_json_atomic(report_path, result)
        return result
    finally:
        temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--report")
    args = parser.parse_args(argv)
    try:
        result = build_smooth_idle_atlas(
            Path(args.source),
            Path(args.output),
            Path(args.report) if args.report else None,
        )
    except AtlasError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
