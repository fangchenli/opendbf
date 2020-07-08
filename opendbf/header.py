from datetime import date
from struct import Struct

from codepage import code_page_map

dbf_file_type_map = {
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
    def __init__(self, file):
        self.fmt = "=BBBBLHH16sBBH"
        super().__init__(self.fmt)
        data = file.read(self.size)
        data_tuple = self.unpack(data)
        self.file_type = dbf_file_type_map[int(hex(data_tuple[0]), 16)]
        self.date = date(data_tuple[1] + 1900, data_tuple[2], data_tuple[3])
        self.num_records, self.header_length, self.record_length = [
            data_tuple[i] for i in (4, 5, 6)
        ]
        self.encoding = code_page_map[int(hex(data_tuple[-2]), 16)]

    def __repr__(self):
        return (
            f"File Type: {self.file_type}\n"
            f"Last Modified: {self.date}\n"
            f"Number of Records: {self.num_records}\n"
            f"Encoding: {self.encoding[1]}\n"
        )
