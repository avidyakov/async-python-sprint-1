import json
from pathlib import Path

import pytest


@pytest.fixture
def response_path() -> Path:
    return Path("examples/response.json")


@pytest.fixture
def response(response_path) -> dict:
    return json.loads(response_path.read_text())
