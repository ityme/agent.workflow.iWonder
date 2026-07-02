import unittest

from iSpace.tools.harness_lib.state_machine import (
    StateTransitionError,
    default_development_transitions,
    ensure_transition,
)


class StateMachineTest(unittest.TestCase):
    def test_default_development_allows_declared_transition(self):
        transitions = default_development_transitions()

        ensure_transition(transitions, "pm", "intake", "clarifying")

    def test_default_development_rejects_illegal_transition(self):
        transitions = default_development_transitions()

        with self.assertRaisesRegex(StateTransitionError, "pm"):
            ensure_transition(transitions, "pm", "intake", "planned")

    def test_unknown_role_fails_closed(self):
        with self.assertRaisesRegex(StateTransitionError, "unknown"):
            ensure_transition({}, "unknown", "running", "exited")


if __name__ == "__main__":
    unittest.main()
