from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class PathPolicyError(ValueError):
    """Raised when a path is outside the harness write policy."""


def find_harness_root(start: str | Path | None = None) -> Path:
    current = Path.cwd() if start is None else Path(start)
    current = current.resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (candidate / "README.md").exists() and (candidate / "track").exists():
            return candidate

    raise PathPolicyError(f"Cannot find harness root from {current}")


@dataclass(frozen=True)
class HarnessPaths:
    root: Path
    allowed_core_write_dirs: tuple[str, ...] = ("track", "tmp", "reports")

    def __post_init__(self) -> None:
        object.__setattr__(self, "root", Path(self.root).resolve())

    def resolve_core_write_path(self, target: str | Path) -> Path:
        resolved = self._resolve_under_root(target)
        relative = self._relative_parts(resolved)
        if not relative or relative[0] not in self.allowed_core_write_dirs:
            allowed = ", ".join(self.allowed_core_write_dirs)
            raise PathPolicyError(f"Core tools may only write under: {allowed}")
        return resolved

    def relative_to_root(self, target: str | Path) -> str:
        resolved = self._resolve_under_root(target)
        return resolved.relative_to(self.root).as_posix()

    def _resolve_under_root(self, target: str | Path) -> Path:
        path = Path(target)
        resolved = path.resolve() if path.is_absolute() else (self.root / path).resolve()
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise PathPolicyError(f"Path escapes harness root: {target}") from exc
        return resolved

    def _relative_parts(self, target: Path) -> tuple[str, ...]:
        return target.relative_to(self.root).parts
