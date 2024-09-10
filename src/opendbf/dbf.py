from csv import QUOTE_MINIMAL, writer
from os import SEEK_CUR, PathLike
from pathlib import Path

from opendbf.header import Header


def dbf_to_csv(file_path: str | PathLike) -> Path:

    # Sanity check
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    assert file_path.exists(), f"File not found: {file_path}."
    assert file_path.is_file(), f"Not a file: {file_path}."
    assert file_path.suffix == ".dbf", f"Not a dbf file: {file_path}."

    with open(file_path, "rb") as file:
        header = Header(file)

        csv_path = file_path.with_suffix(".csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = writer(csv_file, delimiter=",", quoting=QUOTE_MINIMAL)
            csv_writer.writerow(header.field_name)

            for _ in range(header.num_records):
                record = []
                for field in header.field_list:
                    data_bytes = file.read(field.field_length)
                    data_bytes = data_bytes.strip()
                    data_str = data_bytes.decode(header.encoding)
                    record.append(data_str)
                csv_writer.writerow(record)
                file.seek(1, SEEK_CUR)
    return csv_path
