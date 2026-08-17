import json
from pathlib import Path

from jsonschema import validate


SCHEMAS_DIRECTORY = Path(__file__).resolve().parent.parent / "schemas"


def validate_schema(response_body, schema_filename):
    schema_path = SCHEMAS_DIRECTORY / schema_filename

    with schema_path.open(encoding="utf-8") as schema_file:
        schema = json.load(schema_file)

    validate(instance=response_body, schema=schema)
