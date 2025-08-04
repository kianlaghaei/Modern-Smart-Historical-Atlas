from pathlib import Path
from typing import Any

from openai import OpenAI

from models import AtlasDB

client = OpenAI()


def extract_atlas(text: str) -> AtlasDB:
    """Uses OpenAI GPT-4o with function calling to extract structured atlas data."""
    schema = AtlasDB.model_json_schema()
    completion = client.responses.create(
        model="gpt-4o-mini",
        input=f"Extract a historical atlas from this text:\n{text}",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "atlas_schema",
                "schema": schema,
            },
        },
    )
    data: Any = completion.output[0].content[0].json
    return AtlasDB.model_validate(data)
