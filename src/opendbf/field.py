from struct import Struct

field_type_map = {
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

field_flag_map = {
    0x01: "System Column (not visible to user)",
    0x02: "Column can store null values",
    0x04: "Binary column (for CHAR and MEMO only)",
    0x06: "(0x02+0x04) When a field is NULL and binary (Integer, Currency, and Character/Memo fields)",
    0x0C: "Column is autoincrementing",
}


class Field(Struct):
    def __init__(self, file):

        self.fmt = "<11scLBBBLB8s"
        super().__init__(self.fmt)
        data = file.read(self.size)
        data_tuple = self.unpack(data)
        self.field_name = data_tuple[0].decode().replace("\0", "")
        self.field_type = field_type_map[data_tuple[1].decode()]
        self.displacement, self.field_length, self.num_decimal, self.field_flag = [
            data_tuple[i] for i in (2, 3, 4, 5)
        ]
        if self.field_flag:
            self.field_flag = field_flag_map[data_tuple[5]]

    def __repr__(self):
        return (
            f"Field Name: {self.field_name}\n"
            f"Field Type: {self.field_type}\n"
            f"Field Length: {self.field_length}\n"
            f"Field Flag : {self.field_flag}\n"
        )
