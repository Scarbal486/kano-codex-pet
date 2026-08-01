from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw, ImageSequence

from scripts.build_smooth_idle_atlas import (
    AtlasError,
    build_smooth_idle_atlas,
    inspect_animated_webp,
)


ATLAS_SIZE = (1536, 2288)
CELL_SIZE = (192, 208)


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
        top = row * CELL_SIZE[1]
        draw.rectangle((10 + row, top + 10, 30 + row, top + 30), fill=(row, 100, 180, 255))

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
            self.assertEqual(result["durations_ms"], [100] * 6)
            self.assertEqual(result["loop"], 0)
            self.assertEqual(json.loads(report_path.read_text(encoding="utf-8")), result)

            metadata = inspect_animated_webp(output_path)
            self.assertTrue(metadata["animation"])
            self.assertEqual(metadata["loop"], 0)
            self.assertEqual(metadata["durations_ms"], [100] * 6)

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
