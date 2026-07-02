import tempfile
import unittest
from pathlib import Path

from iSpace.tools.harness_lib.audit import audit_run
from iSpace.tools.harness_lib.jsonio import append_jsonl, write_json
from iSpace.tools.harness_lib.paths import HarnessPaths
from iSpace.tools.harness_lib.track import TrackStore


class AuditTest(unittest.TestCase):
    def test_clean_demo_run_has_no_findings(self):
        root = Path(__file__).resolve().parents[1]

        findings = audit_run(HarnessPaths(root), "0001")

        self.assertEqual(findings, [])

    def test_detects_secret_in_track_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            store = TrackStore(HarnessPaths(root))
            run = store.create_run("demo", "default-development")
            secret_file = root / "track" / "runs" / run["run_id"] / "secret.json"
            write_json(secret_file, {"note": "password=123456"})

            findings = audit_run(HarnessPaths(root), run["run_id"])

            self.assertTrue(any("sensitive" in item for item in findings))

    def test_detects_duplicate_event_id_and_bad_reply_to(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            store = TrackStore(HarnessPaths(root))
            run = store.create_run("demo", "default-development")
            timeline = root / "track" / "timeline.jsonl"
            append_jsonl(
                timeline,
                {
                    "event_id": "evt-00000001",
                    "reply_to": "evt-00000000",
                    "run_id": run["run_id"],
                    "summary": "first",
                },
            )
            append_jsonl(
                timeline,
                {
                    "event_id": "evt-00000001",
                    "reply_to": "evt-missing",
                    "run_id": run["run_id"],
                    "summary": "second",
                },
            )

            findings = audit_run(HarnessPaths(root), run["run_id"])

            self.assertTrue(any("duplicate event_id" in item for item in findings))
            self.assertTrue(any("invalid reply_to" in item for item in findings))

    def test_detects_evidence_path_outside_harness_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            store = TrackStore(HarnessPaths(root))
            run = store.create_run("demo", "default-development")
            task = store.create_task(run["run_id"], "demo task")
            result_file = (
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
            write_json(
                result_file,
                {
                    "run_id": run["run_id"],
                    "task_id": task["task_id"],
                    "attempt_id": "attempt-0001",
                    "role": "coder",
                    "result": "success",
                    "summary": "bad evidence",
                    "evidence_refs": ["../outside.txt"],
                    "timestamp": "2026-07-02T00:00:00+00:00",
                },
            )

            findings = audit_run(HarnessPaths(root), run["run_id"])

            self.assertTrue(any("evidence path escapes harness root" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
