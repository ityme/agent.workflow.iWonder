import tempfile
import unittest
from pathlib import Path

from iSpace.tools.harness_lib.atomic import atomic_write_text


class AtomicWriteTest(unittest.TestCase):
    def test_atomic_write_text_creates_parent_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "track" / "0001" / "run.json"

            atomic_write_text(target, '{"run_id":"0001"}\n')

            self.assertEqual(target.read_text(encoding="utf-8"), '{"run_id":"0001"}\n')

    def test_atomic_write_text_replaces_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "reports" / "summary.md"
            target.parent.mkdir()
            target.write_text("old", encoding="utf-8")

            atomic_write_text(target, "new")

            self.assertEqual(target.read_text(encoding="utf-8"), "new")
            self.assertEqual(list(target.parent.glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
