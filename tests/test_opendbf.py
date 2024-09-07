from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import pandas as pd

from opendbf.dbf import dbf_to_csv


def test_read(data_path):
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        with ZipFile(data_path, "r") as zip_file:
            zip_file.extractall(temp_path)

        csv_path = dbf_to_csv(temp_path / "par.dbf")

        df = pd.read_csv(csv_path, dtype={9: str, 14: str, 56: str, 57: str})
        assert df.shape == (127119, 86)
