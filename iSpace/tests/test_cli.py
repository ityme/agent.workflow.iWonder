import subprocess
import sys
import tempfile
import unittest
import os
from pathlib import Path

from iSpace.tools.harness_lib.jsonio import read_json


HARNESS = Path("iSpace") / "tools" / "harness.py"


class HarnessCliTest(unittest.TestCase):
    def run_cli(self, *args, root):
        return subprocess.run(
            [sys.executable, str(HARNESS), "--root", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_new_run_new_task_and_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()

            run = self.run_cli(
                "new-run",
                "--title",
                "示例运行",
                "--profile",
                "default-development",
                root=root,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("0001", run.stdout)

            task = self.run_cli(
                "new-task",
                "--run",
                "0001",
                "--name",
                "登录 API",
                "--acceptance",
                "接口返回 200。",
                root=root,
            )
            self.assertEqual(task.returncode, 0, task.stderr)
            self.assertIn("001_api", task.stdout)

            validate = self.run_cli("validate", "--run", "0001", root=root)
            self.assertEqual(validate.returncode, 0, validate.stderr)
            self.assertIn("valid", validate.stdout)

            run_json = read_json(root / "track" / "runs" / "0001" / "run.json")
            self.assertEqual(run_json["task_ids"], ["001_api"])

    @unittest.skipIf(
        os.environ.get("HARNESS_SELFTEST_RUNNING") == "1",
        "selftest 内部运行 unittest 时跳过递归自检。",
    )
    def test_selftest_runs_without_polluting_requested_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()

            result = self.run_cli("selftest", root=root)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("python -m unittest discover iSpace/tests", result.stdout)
            self.assertIn("demo", result.stdout)
            self.assertFalse((root / "track").exists())


if __name__ == "__main__":
    unittest.main()
