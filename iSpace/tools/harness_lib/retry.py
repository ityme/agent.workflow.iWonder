from __future__ import annotations


def next_attempt_id(existing_count: int) -> str:
    return f"attempt-{existing_count + 1:04d}"
