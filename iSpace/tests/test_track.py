import tempfile
import unittest
from pathlib import Path

from iSpace.tools.harness_lib.jsonio import read_json, read_jsonl
from iSpace.tools.harness_lib.paths import HarnessPaths
from iSpace.tools.harness_lib.track import TrackStore


class TrackStoreTest(unittest.TestCase):
    def test_create_run_is_idempotent_and_writes_timeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            store = TrackStore(HarnessPaths(root))

            first = store.create_run("示例运行", "default-development")
            second = store.create_run("示例运行", "default-development")

            self.assertEqual(first["run_id"], "0001")
            self.assertEqual(second["run_id"], "0001")
            run_file = root / "track" / "runs" / "0001" / "run.json"
            self.assertEqual(read_json(run_file)["title"], "示例运行")
            events = list(read_jsonl(root / "track" / "timeline.jsonl"))
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["event_type"], "run_created")

    def test_create_task_slugifies_name_and_updates_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            store = TrackStore(HarnessPaths(root))
            store.create_run("示例运行", "default-development")

            task = store.create_task(
                "0001",
                "登录 API",
                acceptance_criteria=["接口返回 200。"],
                non_goals=["不发布。"],
            )

            self.assertEqual(task["task_id"], "001_api")
            self.assertEqual(task["acceptance_criteria"], ["接口返回 200。"])
            run = read_json(root / "track" / "runs" / "0001" / "run.json")
            self.assertEqual(run["task_ids"], ["001_api"])
            task_file = root / "track" / "task" / "001_api" / "task.json"
            self.assertTrue(task_file.exists())

    def test_validate_run_detects_schema_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            store = TrackStore(HarnessPaths(root))
            store.create_run("示例运行", "default-development")
            run_path = root / "track" / "runs" / "0001" / "run.json"
            payload = read_json(run_path)
            del payload["title"]
            from iSpace.tools.harness_lib.jsonio import write_json

            write_json(run_path, payload)

            errors = store.validate_run("0001")

            self.assertEqual(len(errors), 1)
            self.assertIn("title", errors[0])

    def test_validate_run_detects_missing_task_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            store = TrackStore(HarnessPaths(root))
            run = store.create_run("示例运行", "default-development")
            run["task_ids"].append("999_missing-task")
            from iSpace.tools.harness_lib.jsonio import write_json

            write_json(root / "track" / "runs" / "0001" / "run.json", run)

            errors = store.validate_run("0001")

            self.assertTrue(any("missing task file" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
