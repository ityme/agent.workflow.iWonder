import unittest
from pathlib import Path

from iSpace.tools.harness_lib.adapter import (
    AdapterCommandRejected,
    assert_command_allowed,
    load_adapter,
)


ROOT = Path(__file__).resolve().parents[1]


class AdapterAllowlistTest(unittest.TestCase):
    def test_builtin_adapter_allows_exact_role_command(self):
        adapter = load_adapter(
            ROOT / "adapters" / "local-python-workers" / "default-development.json"
        )
        command = adapter["roles"]["coder"]["command"]

        assert_command_allowed(adapter, command)

    def test_builtin_adapter_rejects_extra_argument(self):
        adapter = load_adapter(
            ROOT / "adapters" / "local-python-workers" / "default-development.json"
        )
        command = [*adapter["roles"]["coder"]["command"], "--unexpected"]

        with self.assertRaises(AdapterCommandRejected):
            assert_command_allowed(adapter, command)

    def test_all_role_commands_are_allowlisted(self):
        for path in sorted((ROOT / "adapters" / "local-python-workers").glob("*.json")):
            adapter = load_adapter(path)
            for role_config in adapter["roles"].values():
                assert_command_allowed(adapter, role_config["command"])


if __name__ == "__main__":
    unittest.main()
