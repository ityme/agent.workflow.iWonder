import unittest

from iSpace.tools.harness_lib.redact import contains_secret, redact_text


class RedactTest(unittest.TestCase):
    def test_redacts_token_like_values(self):
        text = "api_key=sk-abcdefghijklmnopqrstuvwxyz123456"

        redacted = redact_text(text)

        self.assertNotIn("sk-abcdefghijklmnopqrstuvwxyz123456", redacted)
        self.assertIn("[REDACTED]", redacted)

    def test_detects_secret_words(self):
        self.assertTrue(contains_secret("password=123456"))
        self.assertFalse(contains_secret("普通进度摘要"))


if __name__ == "__main__":
    unittest.main()
