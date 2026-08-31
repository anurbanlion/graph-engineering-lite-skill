import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "apply_patch"


class TemporaryPatchCreationTests(unittest.TestCase):
    def run_applicator(self, patch: Path, target: Path):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(patch), str(target)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

    def test_creates_missing_file_with_zero_line_range(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            patch = root / "change.temp"
            target = root / "created.txt"
            patch.write_text("@@ 1 0\n+first\n+second\n", encoding="utf-8")

            result = self.run_applicator(patch, target)

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), "first\nsecond\n")
            self.assertFalse(patch.exists())

    def test_populates_existing_empty_file_with_zero_line_range(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            patch = root / "change.temp"
            target = root / "empty.txt"
            target.touch()
            patch.write_text("@@ 1 0\n+content\n", encoding="utf-8")

            result = self.run_applicator(patch, target)

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), "content\n")

    def test_rejects_zero_line_range_for_nonempty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            patch = root / "change.temp"
            target = root / "existing.txt"
            target.write_text("existing\n", encoding="utf-8")
            patch.write_text("@@ 1 0\n+replacement\n", encoding="utf-8")

            result = self.run_applicator(patch, target)

            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("Invalid target range: 1-0", result.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), "existing\n")

    def test_creates_missing_file_with_any_single_range(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            patch = root / "change.temp"
            target = root / "missing.txt"
            patch.write_text("@@ 4 8\n+content\n", encoding="utf-8")

            result = self.run_applicator(patch, target)

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), "content\n")
            self.assertFalse(patch.exists())

    def test_rejects_multiple_hunks_for_missing_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            patch = root / "change.temp"
            target = root / "missing.txt"
            patch.write_text("@@ 1 1\n+first\n@@ 2 2\n+second\n", encoding="utf-8")

            result = self.run_applicator(patch, target)

            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("only be created from one patch hunk", result.stdout)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
