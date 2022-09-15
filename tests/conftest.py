import json
from pathlib import Path

import pytest


@pytest.fixture
def response_path() -> Path:
    return Path(__file__).parent.parent / "examples/response.json"


@pytest.fixture
def response(response_path) -> dict:
    return json.loads(response_path.read_text())
