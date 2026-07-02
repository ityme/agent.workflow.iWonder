from __future__ import annotations

from pathlib import Path
from typing import Any

from .jsonio import read_json


class SchemaValidationError(ValueError):
    """Raised when an instance does not match the supported schema subset."""


TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
}


def load_schema(path: str | Path) -> dict[str, Any]:
    schema = read_json(path)
    if not isinstance(schema, dict):
        raise SchemaValidationError("schema root must be an object")
    return schema


def validate_instance(instance: Any, schema: dict[str, Any], path: str = "$") -> None:
    expected_type = schema.get("type")
    if expected_type is not None:
        _validate_type(instance, expected_type, path)

    if "enum" in schema and instance not in schema["enum"]:
        allowed = ", ".join(str(item) for item in schema["enum"])
        raise SchemaValidationError(f"{path}: value {instance!r} not in enum [{allowed}]")

    if isinstance(instance, dict):
        _validate_object(instance, schema, path)
    elif isinstance(instance, list):
        _validate_array(instance, schema, path)


def validate_file(path: str | Path, schema_path: str | Path) -> list[str]:
    try:
        validate_instance(read_json(path), load_schema(schema_path))
    except SchemaValidationError as exc:
        return [str(exc)]
    return []


def _validate_type(instance: Any, expected_type: str | list[str], path: str) -> None:
    expected_types = expected_type if isinstance(expected_type, list) else [expected_type]
    for item in expected_types:
        if item == "integer":
            if isinstance(instance, int) and not isinstance(instance, bool):
                return
        elif item == "number":
            if isinstance(instance, (int, float)) and not isinstance(instance, bool):
                return
        elif item in TYPE_MAP and isinstance(instance, TYPE_MAP[item]):
            return
    raise SchemaValidationError(f"{path}: expected type {expected_type}")


def _validate_object(instance: dict[str, Any], schema: dict[str, Any], path: str) -> None:
    required = schema.get("required", [])
    for field in required:
        if field not in instance:
            raise SchemaValidationError(f"{path}: missing required field {field}")

    properties = schema.get("properties", {})
    for field, field_schema in properties.items():
        if field in instance:
            validate_instance(instance[field], field_schema, f"{path}.{field}")


def _validate_array(instance: list[Any], schema: dict[str, Any], path: str) -> None:
    item_schema = schema.get("items")
    if item_schema is None:
        return
    for index, item in enumerate(instance):
        validate_instance(item, item_schema, f"{path}[{index}]")
