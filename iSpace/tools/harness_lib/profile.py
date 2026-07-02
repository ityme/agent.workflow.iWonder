from __future__ import annotations

from pathlib import Path
from typing import Any

from .jsonio import read_json
from .schema import SchemaValidationError, load_schema, validate_instance


class ProfileError(ValueError):
    """Raised when a profile cannot be loaded or validated."""


def load_profile(path: str | Path) -> dict[str, Any]:
    profile_path = Path(path)
    if not profile_path.exists():
        raise ProfileError(f"profile file not found: {profile_path}")
    profile = read_json(profile_path)
    if not isinstance(profile, dict):
        raise ProfileError(f"profile must be an object: {profile_path}")

    try:
        validate_instance(profile, _profile_schema())
        _validate_flow_roles(profile, profile_path)
    except SchemaValidationError as exc:
        raise ProfileError(f"{profile_path}: {exc}") from exc
    return profile


def load_profiles(root: str | Path) -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}
    for profile_file in sorted(Path(root).glob("*/profile.json")):
        profile = load_profile(profile_file)
        profiles[profile["profile_id"]] = profile
    return profiles


def _validate_flow_roles(profile: dict[str, Any], path: Path) -> None:
    roles = {item.get("role") for item in profile.get("roles", []) if isinstance(item, dict)}
    missing = [role for role in profile.get("flow", []) if role not in roles]
    if missing:
        raise ProfileError(f"{path}: flow references missing roles: {', '.join(missing)}")


def _profile_schema() -> dict[str, Any]:
    return load_schema(Path(__file__).resolve().parents[2] / "schemas" / "profile.schema.json")
