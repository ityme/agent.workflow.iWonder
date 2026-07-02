import unittest

from iSpace.tools.harness_lib.schema import SchemaValidationError, validate_instance


class SchemaSubsetTest(unittest.TestCase):
    def test_validate_required_type_enum_array_and_nested_items(self):
        schema = {
            "type": "object",
            "required": ["state", "items", "meta"],
            "properties": {
                "state": {"type": "string", "enum": ["planned", "running"]},
                "items": {"type": "array", "items": {"type": "string"}},
                "meta": {
                    "type": "object",
                    "required": ["retry_count"],
                    "properties": {"retry_count": {"type": "integer"}},
                },
            },
        }

        validate_instance(
            {"state": "planned", "items": ["a"], "meta": {"retry_count": 0}},
            schema,
        )

    def test_validate_reports_missing_required_field(self):
        schema = {"type": "object", "required": ["run_id"], "properties": {}}

        with self.assertRaisesRegex(SchemaValidationError, "run_id"):
            validate_instance({}, schema)

    def test_validate_reports_enum_and_item_type_errors(self):
        schema = {
            "type": "object",
            "properties": {
                "result": {"type": "string", "enum": ["success", "fail"]},
                "refs": {"type": "array", "items": {"type": "string"}},
            },
        }

        with self.assertRaisesRegex(SchemaValidationError, "result"):
            validate_instance({"result": "maybe", "refs": ["ok"]}, schema)
        with self.assertRaisesRegex(SchemaValidationError, "refs"):
            validate_instance({"result": "success", "refs": [1]}, schema)


if __name__ == "__main__":
    unittest.main()
