import tempfile
import unittest
from pathlib import Path

from iSpace.tools.harness_lib.audit import audit_run
from iSpace.tools.harness_lib.jsonio import write_json
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


if __name__ == "__main__":
    unittest.main()
