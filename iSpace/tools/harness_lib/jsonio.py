from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable, Iterator

from .atomic import atomic_write_text


def read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | Path, payload: Any) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    atomic_write_text(path, f"{text}\n")


def read_jsonl(path: str | Path) -> Iterator[Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                yield json.loads(stripped)


def write_jsonl(path: str | Path, records: Iterable[Any]) -> None:
    lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records]
    atomic_write_text(path, "".join(f"{line}\n" for line in lines))


def append_jsonl(path: str | Path, record: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{line}\n")
        handle.flush()
        os.fsync(handle.fileno())
