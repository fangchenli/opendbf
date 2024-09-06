from csv import QUOTE_MINIMAL, writer
from os import SEEK_CUR

from opendbf.field import Field
from opendbf.header import Header


def dbf_to_csv(file_path: str) -> str:
    csv_path = file_path.replace(".dbf", ".csv")
    with open(file_path, "rb") as file:
        with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = writer(csv_file, delimiter=",", quoting=QUOTE_MINIMAL)

            header = Header(file)
            num_fields = (header.header_length - header.size - 1) // header.size
            field_list = [Field(file) for _ in range(num_fields)]
            field_name = [field.field_name for field in field_list]
            csv_writer.writerow(field_name)

            for _ in range(header.num_records):
                record = []
                for field in field_list:

                    if file.peek(1)[:1] in [b"\r", b"\n"]:
                        file.seek(2, SEEK_CUR)

                    data = file.read(field.field_length)
                    data = data.strip()
                    try:
                        data = data.decode("utf-8")
                    except UnicodeDecodeError:
                        data = data.decode("ISO-8859-1")
                    record.append(data)
                csv_writer.writerow(record)
                file.seek(1, SEEK_CUR)
    return csv_path
