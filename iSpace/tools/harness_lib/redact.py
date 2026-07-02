from __future__ import annotations

import re


SECRET_PATTERNS = [
    re.compile(r"(?i)(password|passwd|api[_-]?key|token|secret)\s*[:=]\s*[^,\s\"']+"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
]


def redact_text(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def contains_secret(text: str) -> bool:
    return redact_text(text) != text
