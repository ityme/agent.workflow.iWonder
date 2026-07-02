import tempfile
import unittest
from pathlib import Path

from iSpace.tools.harness_lib.jsonio import (
    append_jsonl,
    read_json,
    read_jsonl,
    write_json,
)


class JsonIoTest(unittest.TestCase):
    def test_write_and_read_json_are_utf8_and_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "track" / "run.json"
            payload = {"run_id": "0001", "title": "中文标题"}

            write_json(target, payload)

            self.assertEqual(read_json(target), payload)
            text = target.read_text(encoding="utf-8")
            self.assertIn('"title": "中文标题"', text)
            self.assertTrue(text.endswith("\n"))

    def test_append_and_read_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "track" / "progress.jsonl"

            append_jsonl(target, {"event_id": "evt-00000001"})
            append_jsonl(target, {"event_id": "evt-00000002"})

            self.assertEqual(
                list(read_jsonl(target)),
                [{"event_id": "evt-00000001"}, {"event_id": "evt-00000002"}],
            )

    def test_read_jsonl_ignores_blank_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "events.jsonl"
            target.write_text('{"a": 1}\n\n{"b": 2}\n', encoding="utf-8")

            self.assertEqual(list(read_jsonl(target)), [{"a": 1}, {"b": 2}])


if __name__ == "__main__":
    unittest.main()
