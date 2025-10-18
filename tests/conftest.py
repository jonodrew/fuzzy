import os
import shutil
import tempfile

import pytest
from starlette.testclient import TestClient

from tech_test.app.main import app_factory


@pytest.fixture
def client() -> TestClient:
    return TestClient(app_factory())


def good_data() -> dict:
    return {
        "input_language": "en",
        "output_language": "fr",
        "input_text": "Hello world!",
    }


@pytest.fixture(scope="function", autouse=True)
def hf_cache_dir(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp_cache_dir:
        # Override the HF cache env vars
        monkeypatch.setenv("HF_HOME", tmp_cache_dir)
        monkeypatch.setenv("TRANSFORMERS_CACHE", tmp_cache_dir)

        cache_path = os.path.expanduser("~/.cache/huggingface/hub")
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path, ignore_errors=True)

        yield tmp_cache_dir
        cache_path = os.path.expanduser("~/.cache/huggingface/hub")
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
