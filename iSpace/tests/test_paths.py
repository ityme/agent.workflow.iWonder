import tempfile
import unittest
from pathlib import Path

from iSpace.tools.harness_lib.paths import (
    HarnessPaths,
    PathPolicyError,
    find_harness_root,
)


class HarnessPathsTest(unittest.TestCase):
    def test_find_harness_root_from_nested_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            nested = root / "tools" / "harness_lib"
            nested.mkdir(parents=True)
            (root / "track").mkdir()
            (root / "README.md").write_text("# demo\n", encoding="utf-8")

            self.assertEqual(find_harness_root(nested), root.resolve())

    def test_resolve_write_path_allows_core_output_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            paths = HarnessPaths(root)

            target = paths.resolve_core_write_path("track/0001/run.json")

            self.assertEqual(target, (root / "track" / "0001" / "run.json").resolve())

    def test_resolve_write_path_rejects_docs_and_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            paths = HarnessPaths(root)

            with self.assertRaises(PathPolicyError):
                paths.resolve_core_write_path("docs/00-overview.md")
            with self.assertRaises(PathPolicyError):
                paths.resolve_core_write_path("../outside.json")

    def test_relative_to_root_uses_posix_separator(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "iSpace"
            root.mkdir()
            paths = HarnessPaths(root)

            rel = paths.relative_to_root(root / "track" / "0001" / "run.json")

            self.assertEqual(rel, "track/0001/run.json")


if __name__ == "__main__":
    unittest.main()
