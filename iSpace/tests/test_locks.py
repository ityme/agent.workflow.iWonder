import tempfile
import time
import unittest
from pathlib import Path

from iSpace.tools.harness_lib.locks import FileLock, LockTimeout


class FileLockTest(unittest.TestCase):
    def test_lock_creates_and_removes_lock_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock_path = Path(tmp) / "tmp" / "run.lock"

            with FileLock(lock_path, timeout_seconds=0.2):
                self.assertTrue(lock_path.exists())

            self.assertFalse(lock_path.exists())

    def test_second_lock_times_out_while_first_is_held(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock_path = Path(tmp) / "tmp" / "run.lock"

            with FileLock(lock_path, timeout_seconds=0.2):
                with self.assertRaises(LockTimeout):
                    with FileLock(lock_path, timeout_seconds=0.05, poll_interval=0.01):
                        pass

    def test_stale_lock_can_be_recovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock_path = Path(tmp) / "tmp" / "run.lock"
            lock_path.parent.mkdir()
            lock_path.write_text("stale", encoding="utf-8")
            old_time = time.time() - 60
            lock_path.touch()
            import os

            os.utime(lock_path, (old_time, old_time))

            with FileLock(lock_path, timeout_seconds=0.2, stale_seconds=1):
                self.assertTrue(lock_path.exists())

            self.assertFalse(lock_path.exists())


if __name__ == "__main__":
    unittest.main()
