from __future__ import annotations

from typing import Mapping


class StateTransitionError(ValueError):
    """Raised when a role attempts an undeclared state transition."""


Transitions = Mapping[str, Mapping[str, tuple[str, ...]]]


def default_development_transitions() -> dict[str, dict[str, tuple[str, ...]]]:
    return {
        "pm": {
            "intake": ("clarifying",),
            "clarifying": ("ready_for_builder",),
            "ready_for_builder": ("waiting_builder",),
            "waiting_builder": ("waiting_user_ack",),
            "waiting_user_ack": ("exited",),
        },
        "builder": {
            "planned": ("waiting_pm_ack",),
            "waiting_pm_ack": ("exited",),
        },
        "tm": {
            "planned": ("running",),
            "running": ("waiting_coder",),
            "waiting_coder": ("waiting_tester",),
            "waiting_tester": ("waiting_opser",),
            "waiting_opser": ("waiting_ack",),
            "waiting_ack": ("exited",),
        },
        "coder": {
            "running": ("waiting_tm_ack",),
            "waiting_tm_ack": ("exited",),
        },
        "tester": {
            "running": ("waiting_tm_ack",),
            "waiting_tm_ack": ("exited",),
        },
        "opser": {
            "running": ("waiting_tm_ack",),
            "waiting_tm_ack": ("exited",),
        },
    }


def ensure_transition(
    transitions: Transitions,
    role: str,
    from_state: str,
    to_state: str,
) -> None:
    role_transitions = transitions.get(role)
    if role_transitions is None:
        raise StateTransitionError(f"unknown role {role}")
    allowed = role_transitions.get(from_state, ())
    if to_state not in allowed:
        allowed_text = ", ".join(allowed) if allowed else "none"
        raise StateTransitionError(
            f"{role}: illegal transition {from_state} -> {to_state}; allowed: {allowed_text}"
        )
