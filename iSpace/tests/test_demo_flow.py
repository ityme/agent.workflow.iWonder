import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from iSpace.tools.harness_lib.jsonio import read_json


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "tools" / "harness.py"


class DemoFlowTest(unittest.TestCase):
    def test_demo_runs_default_development_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()

            demo = subprocess.run(
                [sys.executable, str(HARNESS), "--root", str(root), "demo"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(demo.returncode, 0, demo.stderr)
            self.assertIn("demo run 0001", demo.stdout)

            validate = subprocess.run(
                [sys.executable, str(HARNESS), "--root", str(root), "validate", "--run", "0001"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(validate.returncode, 0, validate.stderr)

            run = read_json(root / "track" / "runs" / "0001" / "run.json")
            self.assertEqual(run["task_ids"], ["001_demo-task"])
            result = read_json(
                root
                / "track"
                / "task"
                / "001_demo-task"
                / "tm"
                / "0001"
                / "opser"
                / "attempt-0001"
                / "result.json"
            )
            self.assertEqual(result["result"], "success")


if __name__ == "__main__":
    unittest.main()
