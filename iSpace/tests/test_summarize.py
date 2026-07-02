import tempfile
import unittest
from pathlib import Path

from iSpace.tools.harness_lib.paths import HarnessPaths
from iSpace.tools.harness_lib.summarize import summarize_run
from iSpace.tools.harness_lib.track import TrackStore


class SummarizeTest(unittest.TestCase):
    def test_writes_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            store = TrackStore(HarnessPaths(root))
            run = store.create_run("demo", "default-development")

            report = summarize_run(HarnessPaths(root), run["run_id"])

            self.assertTrue(report.exists())
            text = report.read_text(encoding="utf-8")
            self.assertIn("# Run 0001 摘要", text)
            self.assertIn("demo", text)


if __name__ == "__main__":
    unittest.main()
