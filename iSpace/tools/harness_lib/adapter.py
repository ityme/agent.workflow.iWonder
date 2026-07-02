from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from .jsonio import read_json
from .schema import SchemaValidationError, load_schema, validate_instance


class AdapterError(ValueError):
    """Raised when an adapter cannot be loaded or validated."""


class AdapterCommandRejected(AdapterError):
    """Raised when a command is not exactly present in adapter allowlist."""


def load_adapter(path: str | Path) -> dict[str, Any]:
    adapter_path = Path(path)
    if not adapter_path.exists():
        raise AdapterError(f"adapter file not found: {adapter_path}")
    adapter = read_json(adapter_path)
    if not isinstance(adapter, dict):
        raise AdapterError(f"adapter must be an object: {adapter_path}")

    try:
        validate_instance(adapter, _adapter_schema())
        _validate_role_commands(adapter)
    except SchemaValidationError as exc:
        raise AdapterError(f"{adapter_path}: {exc}") from exc
    return adapter


def assert_command_allowed(adapter: dict[str, Any], command: Sequence[str]) -> None:
    command_list = list(command)
    allowlist = adapter.get("allowlist", [])
    if command_list not in allowlist:
        raise AdapterCommandRejected(f"command is not allowlisted: {command_list}")


def _validate_role_commands(adapter: dict[str, Any]) -> None:
    roles = adapter.get("roles", {})
    if not isinstance(roles, dict):
        raise AdapterError("adapter roles must be an object")
    for role, config in roles.items():
        if not isinstance(config, dict):
            raise AdapterError(f"role config must be an object: {role}")
        command = config.get("command")
        if not isinstance(command, list) or not all(isinstance(item, str) for item in command):
            raise AdapterError(f"role command must be a string array: {role}")
        assert_command_allowed(adapter, command)


def _adapter_schema() -> dict[str, Any]:
    return load_schema(Path(__file__).resolve().parents[2] / "schemas" / "adapter.schema.json")
