import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "apply_patch"
NL = chr(10)




def lines(*values):
    return NL.join(values) + NL


class ApplyPatchTests(unittest.TestCase):
    def run_apply_patch(self, cwd, args=None, stdin=None):
        command = [sys.executable, str(SCRIPT)]
        if args:
            command.extend(args)
        return subprocess.run(
            command,
            cwd=cwd,
            input=stdin,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

    def test_prepared_patch_creates_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            prepared_input = lines(
                "read note.md 1 1",
                "@@",
                "+```bash",
                "+ls -la",
                "+```",
            )

            result = self.run_apply_patch(tmp, stdin=prepared_input)

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(Path(tmp, "note.md").read_text(), NL.join(["```bash", "ls -la", "```"]))
            self.assertIn("M  note.md", result.stdout)

    def test_default_stdin_uses_prepared_patch_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "sample.txt").write_text(lines("hello", "old", "bye"))
            prepared_input = lines(
                "read sample.txt 2 2",
                "@@",
                "+new",
            )

            result = self.run_apply_patch(tmp, stdin=prepared_input)

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(Path(tmp, "sample.txt").read_text(), lines("hello", "new", "bye"))
            self.assertIn("M  sample.txt", result.stdout)
            self.assertIn("-old", result.stdout)

    def test_write_argument_is_not_a_supported_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_apply_patch(tmp, ["--write", "note.md"])

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("Usage: ", result.stdout)
            self.assertIn(" OR ", result.stdout)
            self.assertIn(" -- command args...", result.stdout)
            self.assertFalse(Path(tmp, "note.md").exists())
            self.assertIn("Not tracked", result.stdout)

    def test_prepared_patch_updates_multiple_hunks_in_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "sample.txt").write_text(lines("first", "old a", "middle", "old b", "last"))
            prepared_input = lines(
                "read sample.txt 2 2 4 4",
                "@@",
                "+new a",
                "@@",
                "+new b",
            )

            result = self.run_apply_patch(tmp, stdin=prepared_input)

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(Path(tmp, "sample.txt").read_text(), lines("first", "new a", "middle", "new b", "last"))
            self.assertIn("M  sample.txt", result.stdout)
            self.assertIn("-old a", result.stdout)
            self.assertIn("-old b", result.stdout)

    def test_command_mode_runs_command_without_tree_diff(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_apply_patch(tmp, ["--", "mkdir", "inbox"])

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertTrue(Path(tmp, "inbox").is_dir())
            self.assertIn("Not tracked", result.stdout)


if __name__ == "__main__":
    unittest.main()
