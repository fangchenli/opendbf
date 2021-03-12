from pathlib import Path

import pandas as pd
import pytest

from opendbf.dbf import dbf_to_csv


def test_read():
    root_path = Path(__file__).parent.parent
    data_path = Path(root_path, "data", "par_3-1-21.dbf")
    assert data_path.exists()

    csv_path = dbf_to_csv(str(data_path))

    with pytest.warns(None):
        pd.read_csv(csv_path, dtype={9: str, 14: str, 56: str, 57: str})
