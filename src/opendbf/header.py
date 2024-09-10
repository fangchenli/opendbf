from datetime import date
from io import BufferedReader
from struct import Struct

from opendbf.field import Field

# source: http://shapelib.maptools.org/codepage.html
# {ID: (Codepage, Description)}
code_page_map: dict[int, tuple[str, str]] = {0x57: ("Current ANSI CP", "ANSI")}

encoding_map = {"ANSI": "cp1252"}

dbf_file_type_map: dict[int, str] = {
    0x2: "FoxBASE",
    0x3: "FoxBASE+/Dbase III plus, no memory",
    0x30: "Visual FoxPro",
    0x31: "Visual FoxPro, autoincrement enabled",
    0x32: "Visual FoxPro with field type Varchar or Varbinary",
    0x43: "dBASE IV SQL table files, no memo",
    0x63: "dBASE IV SQL system files, no memo",
    0x83: "FoxBASE+/dBASE III PLUS, with memo",
    0x8B: "dBASE IV with memo",
    0xCB: "dBASE IV SQL table files, with memo",
    0xF5: "FoxPro 2.x (or earlier) with memo",
    0xE5: "HiPer-Six format with SMT memo file",
    0xFB: "FoxBASE",
}


class Header(Struct):
    def __init__(self, file: BufferedReader):
        self.fmt = "=BBBBLHH16sBBH"
        super().__init__(self.fmt)
        data: bytes = file.read(self.size)
        data_tuple = self.unpack(data)
        self.file_type: str = dbf_file_type_map[data_tuple[0]]
        self.date: date = date(data_tuple[1] + 1900, data_tuple[2], data_tuple[3])
        self.num_records, self.header_length, self.record_length = [
            data_tuple[i] for i in (4, 5, 6)
        ]
        self.encoding: str = encoding_map.get(code_page_map[data_tuple[-2]][1], "utf-8")
        self.num_fields: int = (self.header_length - self.size - 1) // self.size
        self.field_list: list[Field] = [
            Field(file, self.encoding) for _ in range(self.num_fields)
        ]
        self.field_name: list[str] = [field.field_name for field in self.field_list]

    def __repr__(self):
        return (
            f"File Type: {self.file_type}\n"
            f"Last Modified: {self.date}\n"
            f"Number of Records: {self.num_records}\n"
            f"Encoding: {self.encoding}\n"
        )
