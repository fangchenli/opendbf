from pathlib import Path

import pytest


@pytest.fixture
def data_path():
    data_dir_path = Path(__file__).parent.parent / "data"
    assert data_dir_path.exists(), f"Data directory not found: {data_dir_path}"
    data_file_path = data_dir_path / "par.zip"
    assert data_file_path.exists(), f"Data file not found: {data_file_path}"
    return data_file_path
