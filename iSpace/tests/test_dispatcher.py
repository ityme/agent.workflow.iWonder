import tempfile
import unittest
from pathlib import Path

from iSpace.tools.harness_lib.adapter import load_adapter
from iSpace.tools.harness_lib.dispatcher import dispatch_role
from iSpace.tools.harness_lib.jsonio import read_json
from iSpace.tools.harness_lib.paths import HarnessPaths
from iSpace.tools.harness_lib.track import TrackStore


ROOT = Path(__file__).resolve().parents[1]


class DispatcherTest(unittest.TestCase):
    def test_dispatch_role_runs_worker_and_records_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            store = TrackStore(HarnessPaths(root))
            run = store.create_run("demo", "default-development")
            task = store.create_task(run["run_id"], "demo task")
            adapter = load_adapter(ROOT / "adapters" / "local-python-workers" / "default-development.json")

            result = dispatch_role(
                harness_root=ROOT,
                store=store,
                adapter=adapter,
                run_id=run["run_id"],
                task_id=task["task_id"],
                role="coder",
            )

            self.assertEqual(result["exit_code"], 0)
            self.assertEqual(result["result"]["result"], "success")
            result_path = (
                root
                / "track"
                / "task"
                / task["task_id"]
                / "tm"
                / run["run_id"]
                / "coder"
                / "attempt-0001"
                / "result.json"
            )
            self.assertEqual(read_json(result_path)["role"], "coder")


if __name__ == "__main__":
    unittest.main()
