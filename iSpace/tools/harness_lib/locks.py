from __future__ import annotations

import os
import time
from pathlib import Path


class LockTimeout(TimeoutError):
    """Raised when a lock cannot be acquired before timeout."""


class FileLock:
    def __init__(
        self,
        path: str | Path,
        timeout_seconds: float = 10.0,
        poll_interval: float = 0.05,
        stale_seconds: float | None = None,
    ) -> None:
        self.path = Path(path)
        self.timeout_seconds = timeout_seconds
        self.poll_interval = poll_interval
        self.stale_seconds = stale_seconds
        self._acquired = False

    def __enter__(self) -> "FileLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout_seconds
        while True:
            self._remove_if_stale()
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise LockTimeout(f"Timed out waiting for lock: {self.path}")
                time.sleep(self.poll_interval)
                continue

            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(f"pid={os.getpid()}\n")
                handle.write(f"created_at={time.time()}\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._acquired = True
            return

    def release(self) -> None:
        if not self._acquired:
            return
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
        finally:
            self._acquired = False

    def _remove_if_stale(self) -> None:
        if self.stale_seconds is None or not self.path.exists():
            return
        try:
            age = time.time() - self.path.stat().st_mtime
        except FileNotFoundError:
            return
        if age >= self.stale_seconds:
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass
