from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageSequence

from scripts.build_smooth_idle_atlas import (
    AtlasError,
    build_smooth_idle_atlas,
    inspect_animated_webp,
)


ATLAS_SIZE = (1536, 2288)
CELL_SIZE = (192, 208)
JUMPING_ROW = 4
WORKING_ROW = 7
GROUND_BOTTOM = 203
TOP_MARGIN = 5
EXPECTED_WORKING_BBOXES = [
    (24, 21, 167, 203),
    (21, 21, 171, 203),
    (26, 21, 166, 203),
    (26, 21, 166, 203),
    (26, 21, 165, 203),
    (27, 21, 165, 203),
]
EXPECTED_JUMPING_BBOXES = [
    (24, 49, 169, 203),
    (27, 5, 165, 180),
    (21, 5, 171, 177),
    (26, 15, 167, 199),
    (40, 16, 153, 203),
]


def make_static_atlas(path: Path) -> Image.Image:
    atlas = Image.new("RGBA", ATLAS_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(atlas)
    for column in range(6):
        left = column * CELL_SIZE[0]
        color = (30 + column * 30, 80 + column * 20, 210 - column * 20, 255)
        draw.rectangle((left + 20, 20, left + 70, 90), fill=color)
        draw.point((left + 100 + column, 120 + column), fill=(255, column, 80, 128))

    neutral_left = 6 * CELL_SIZE[0]
    draw.rectangle(
        (neutral_left + 30, 30, neutral_left + 90, 100),
        fill=(240, 200, 30, 255),
    )
    for row in range(1, 11):
        if row in {JUMPING_ROW, WORKING_ROW}:
            continue
        top = row * CELL_SIZE[1]
        draw.rectangle((10 + row, top + 10, 30 + row, top + 30), fill=(row, 100, 180, 255))

    atlas.save(path, format="PNG")
    return atlas


def make_complex_static_atlas(path: Path) -> Image.Image:
    y, x = np.indices((ATLAS_SIZE[1], ATLAS_SIZE[0]), dtype=np.int32)
    rgba = np.zeros((ATLAS_SIZE[1], ATLAS_SIZE[0], 4), dtype=np.uint8)
    local_x = x % CELL_SIZE[0]
    local_y = y % CELL_SIZE[1]
    visible = (
        ((local_x - 96) ** 2 + (local_y - 104) ** 2 < 72**2)
        | ((local_x > 30) & (local_x < 155) & (local_y > 45) & (local_y < 165))
    )
    rgba[..., 0][visible] = ((x[visible] * 17 + y[visible] * 3) % 256).astype(np.uint8)
    rgba[..., 1][visible] = ((x[visible] * 5 + y[visible] * 13) % 256).astype(np.uint8)
    rgba[..., 2][visible] = ((x[visible] * 11 + y[visible] * 7) % 256).astype(np.uint8)
    rgba[..., 3][visible] = np.where(
        ((local_x[visible] + local_y[visible]) % 9) == 0,
        128,
        255,
    ).astype(np.uint8)
    image = Image.fromarray(rgba, mode="RGBA")
    image.save(path, format="PNG")
    return image


def make_scale_static_atlas(path: Path) -> Image.Image:
    atlas = make_static_atlas(path)
    draw = ImageDraw.Draw(atlas)

    working_bboxes = [
        (18, 5, 173, 203),
        (14, 5, 177, 203),
        (20, 5, 172, 203),
        (20, 5, 172, 203),
        (20, 5, 171, 203),
        (21, 5, 171, 203),
    ]
    for column, (left, top, right, bottom) in enumerate(working_bboxes):
        offset = column * CELL_SIZE[0]
        draw.rectangle(
            (
                offset + left,
                WORKING_ROW * CELL_SIZE[1] + top,
                offset + right - 1,
                WORKING_ROW * CELL_SIZE[1] + bottom - 1,
            ),
            fill=(220, 80 + column * 10, 40, 255),
        )

    jumping_bboxes = [
        (33, 69, 159, 203),
        (36, 28, 156, 180),
        (31, 5, 161, 155),
        (34, 39, 157, 199),
        (47, 40, 145, 203),
    ]
    for column, (left, top, right, bottom) in enumerate(jumping_bboxes):
        offset = column * CELL_SIZE[0]
        draw.rectangle(
            (
                offset + left,
                JUMPING_ROW * CELL_SIZE[1] + top,
                offset + right - 1,
                JUMPING_ROW * CELL_SIZE[1] + bottom - 1,
            ),
            fill=(40, 120 + column * 10, 220, 255),
        )

    atlas.save(path, format="PNG")
    return atlas


class BuildSmoothIdleAtlasTest(unittest.TestCase):
    def test_builds_six_lossless_phases_and_preserves_non_idle_pixels(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "source.png"
            output_path = root / "animated.webp"
            report_path = root / "report.json"
            source = make_static_atlas(source_path)

            result = build_smooth_idle_atlas(source_path, output_path, report_path)

            self.assertTrue(result["ok"])
            self.assertEqual(result["frame_count"], 6)
            self.assertEqual(result["durations_ms"], [100, 4600, 100, 100, 100, 100])
            self.assertEqual(result["loop"], 0)
            self.assertEqual(json.loads(report_path.read_text(encoding="utf-8")), result)

            metadata = inspect_animated_webp(output_path)
            self.assertTrue(metadata["animation"])
            self.assertEqual(metadata["loop"], 0)
            self.assertEqual(metadata["durations_ms"], [100, 4600, 100, 100, 100, 100])

            with Image.open(output_path) as opened:
                self.assertTrue(opened.is_animated)
                self.assertEqual(opened.n_frames, 6)
                frames = [frame.convert("RGBA").copy() for frame in ImageSequence.Iterator(opened)]

            cell_width, cell_height = CELL_SIZE
            for phase, frame in enumerate(frames):
                expected_idle = source.crop(
                    (phase * cell_width, 0, (phase + 1) * cell_width, cell_height)
                ).tobytes()
                for column in range(6):
                    actual_idle = frame.crop(
                        (column * cell_width, 0, (column + 1) * cell_width, cell_height)
                    ).tobytes()
                    self.assertEqual(actual_idle, expected_idle)

                self.assertEqual(
                    frame.crop((6 * cell_width, 0, ATLAS_SIZE[0], cell_height)).tobytes(),
                    source.crop((6 * cell_width, 0, ATLAS_SIZE[0], cell_height)).tobytes(),
                )
                self.assertEqual(
                    frame.crop((0, cell_height, *ATLAS_SIZE)).tobytes(),
                    source.crop((0, cell_height, *ATLAS_SIZE)).tobytes(),
                )

    def test_scales_working_and_jumping_rows_with_balanced_registration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "source.png"
            output_path = root / "animated.webp"
            source = make_scale_static_atlas(source_path)

            result = build_smooth_idle_atlas(source_path, output_path)

            self.assertIn("non_target_rows", result["preservation"])
            self.assertEqual(
                result["preservation"]["non_target_rows"],
                "pixel-identical",
            )
            self.assertNotIn("non_idle_rows", result["preservation"])
            self.assertNotIn("fps", result)

            with Image.open(output_path) as opened:
                frames = [
                    frame.convert("RGBA").copy()
                    for frame in ImageSequence.Iterator(opened)
                ]

            self.assertEqual(len(frames), 6)
            for frame in frames:
                for column, expected_bbox in enumerate(EXPECTED_WORKING_BBOXES):
                    cell = frame.crop(
                        (
                            column * CELL_SIZE[0],
                            WORKING_ROW * CELL_SIZE[1],
                            (column + 1) * CELL_SIZE[0],
                            (WORKING_ROW + 1) * CELL_SIZE[1],
                        )
                    )
                    self.assertEqual(cell.getchannel("A").getbbox(), expected_bbox)
                    self.assertEqual(expected_bbox[3], GROUND_BOTTOM)

                for column, expected_bbox in enumerate(EXPECTED_JUMPING_BBOXES):
                    cell = frame.crop(
                        (
                            column * CELL_SIZE[0],
                            JUMPING_ROW * CELL_SIZE[1],
                            (column + 1) * CELL_SIZE[0],
                            (JUMPING_ROW + 1) * CELL_SIZE[1],
                        )
                    )
                    self.assertEqual(cell.getchannel("A").getbbox(), expected_bbox)
                    self.assertGreaterEqual(expected_bbox[1], TOP_MARGIN)
                    self.assertLessEqual(expected_bbox[3], GROUND_BOTTOM)

                for row in (1, 2, 3, 5, 6, 8, 9, 10):
                    actual = frame.crop(
                        (
                            0,
                            row * CELL_SIZE[1],
                            ATLAS_SIZE[0],
                            (row + 1) * CELL_SIZE[1],
                        )
                    )
                    expected = source.crop(
                        (
                            0,
                            row * CELL_SIZE[1],
                            ATLAS_SIZE[0],
                            (row + 1) * CELL_SIZE[1],
                        )
                    )
                    self.assertEqual(actual.tobytes(), expected.tobytes())

    def test_rejects_wrong_dimensions_without_overwriting_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "wrong.png"
            output_path = root / "existing.webp"
            Image.new("RGBA", (10, 10), (0, 0, 0, 0)).save(source_path)
            output_path.write_bytes(b"keep-me")

            with self.assertRaisesRegex(AtlasError, "1536x2288"):
                build_smooth_idle_atlas(source_path, output_path)

            self.assertEqual(output_path.read_bytes(), b"keep-me")

    def test_complex_transparent_pixels_keep_zero_rgb(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "complex.png"
            output_path = root / "animated.webp"
            make_complex_static_atlas(source_path)

            result = build_smooth_idle_atlas(source_path, output_path)

            self.assertEqual(result["transparent_rgb_residue_pixels"], 0)
            with Image.open(output_path) as opened:
                for frame in ImageSequence.Iterator(opened):
                    rgba = np.asarray(frame.convert("RGBA"))
                    transparent = rgba[..., 3] == 0
                    self.assertTrue(np.all(rgba[..., :3][transparent] == 0))

    def test_rejects_animated_source_without_creating_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "animated-source.webp"
            output_path = root / "output.webp"
            first = Image.new("RGBA", (4, 4), (255, 0, 0, 255))
            second = Image.new("RGBA", (4, 4), (0, 0, 255, 255))
            first.save(
                source_path,
                format="WEBP",
                save_all=True,
                append_images=[second],
                duration=100,
                loop=0,
                lossless=True,
            )

            with self.assertRaisesRegex(AtlasError, "static"):
                build_smooth_idle_atlas(source_path, output_path)

            self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
