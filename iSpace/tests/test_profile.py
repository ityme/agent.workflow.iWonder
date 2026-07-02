import unittest
from pathlib import Path

from iSpace.tools.harness_lib.profile import (
    ProfileError,
    load_profile,
    load_profiles,
)


ROOT = Path(__file__).resolve().parents[1]


class ProfileTest(unittest.TestCase):
    def test_loads_all_builtin_profiles(self):
        profiles = load_profiles(ROOT / "profiles")

        self.assertEqual(
            set(profiles),
            {"default-development", "documentation", "data-analysis", "ops-change"},
        )
        self.assertEqual(profiles["default-development"]["flow"][:3], ["pm", "builder", "tm"])

    def test_profile_roles_match_flow(self):
        profile = load_profile(ROOT / "profiles" / "documentation" / "profile.json")
        roles = {item["role"] for item in profile["roles"]}

        self.assertTrue(set(profile["flow"]).issubset(roles))

    def test_missing_profile_file_is_error(self):
        with self.assertRaises(ProfileError):
            load_profile(ROOT / "profiles" / "missing" / "profile.json")


if __name__ == "__main__":
    unittest.main()
