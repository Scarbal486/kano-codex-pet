#!/usr/bin/env python3
"""Build and validate a 10 FPS animated idle atlas for a Codex Pet v2."""

from __future__ import annotations

import argparse
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
FRAME_DURATION_MS = 100


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


def _build_frames(source: Image.Image) -> list[Image.Image]:
    frames: list[Image.Image] = []
    for phase in range(IDLE_FRAME_COUNT):
        frame = source.copy()
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
    expected_durations = [FRAME_DURATION_MS] * IDLE_FRAME_COUNT
    if not metadata["animation"]:
        raise AtlasError("output WebP is not animated")
    if metadata["loop"] != 0:
        raise AtlasError(f"output loop must be 0, got {metadata['loop']}")
    if metadata["durations_ms"] != expected_durations:
        raise AtlasError(
            f"output durations must be {expected_durations}, "
            f"got {metadata['durations_ms']}"
        )

    neutral_and_unused = source.crop(
        (IDLE_FRAME_COUNT * CELL_WIDTH, 0, ATLAS_WIDTH, CELL_HEIGHT)
    )
    non_idle = source.crop((0, CELL_HEIGHT, ATLAS_WIDTH, ATLAS_HEIGHT))
    frame_count = 0
    residue_counts: list[int] = []
    try:
        with Image.open(path) as opened:
            if not getattr(opened, "is_animated", False):
                raise AtlasError("decoded output is not animated")
            if opened.n_frames != IDLE_FRAME_COUNT:
                raise AtlasError(
                    f"decoded output must have {IDLE_FRAME_COUNT} frames, "
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
                    non_idle,
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
        "fps": 1000 // FRAME_DURATION_MS,
        "loop": metadata["loop"],
        "transparent_rgb_residue_pixels": max(residue_counts, default=0),
        "preservation": {
            "idle_phase_mapping": "passed",
            "neutral_and_unused_cells": "pixel-identical",
            "non_idle_rows": "pixel-identical",
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
        frames[0].save(
            temporary,
            format="WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=[FRAME_DURATION_MS] * IDLE_FRAME_COUNT,
            loop=0,
            background=(0, 0, 0, 0),
            lossless=True,
            quality=100,
            alpha_quality=100,
            method=6,
            minimize_size=True,
        )
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
