from io import BufferedReader
from struct import Struct

type_map = {
    "C": "Character",
    "Y": "Currency",
    "N": "Numeric",
    "F": "Float",
    "D": "Date",
    "T": "DateTime",
    "B": "Double",
    "I": "Integer",
    "L": "Logical",
    "M": "Memo",
    "G": "General",
    "P": "Picture",
    "+": "Autoincrement (dBase Level 7)",
    "O": "Double (dBase Level 7)",
    "@": "Timestamp (dBase Level 7)",
    "V": "Varchar type (Visual Foxpro)",
}

flag_map = {
    0x01: "System Column (not visible to user)",
    0x02: "Column can store null values",
    0x04: "Binary column (for CHAR and MEMO only)",
    0x06: "(0x02+0x04) When a field is NULL and binary (Integer, Currency, and Character/Memo fields)",
    0x0C: "Column is autoincrementing",
}


class Field(Struct):
    def __init__(self, file: BufferedReader, encoding: str):

        self.fmt = "<11scLBBBLB8s"
        super().__init__(self.fmt)
        data = file.read(self.size)
        data_tuple = self.unpack(data)
        self.name = data_tuple[0].decode(encoding).replace("\0", "")
        self.type = type_map[data_tuple[1].decode(encoding)]
        self.displacement, self.length, self.num_decimal, self.flag = [
            data_tuple[i] for i in (2, 3, 4, 5)
        ]
        if self.flag:
            self.flag = flag_map[data_tuple[5]]

    def __repr__(self):
        return (
            f"Field Name: {self.name}\n"
            f"Field Type: {self.type}\n"
            f"Field Length: {self.length}\n"
            f"Field Flag : {self.flag}\n"
        )
