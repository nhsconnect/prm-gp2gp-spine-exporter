from io import BytesIO
from typing import List


def build_csv_contents(header: List, rows: List) -> str:
    def build_line(values):
        return ",".join(values)

    header_line = build_line(header)
    row_lines = [build_line(row) for row in rows]

    return "\n".join([header_line] + row_lines)


def build_bytes_io_contents(data: str) -> BytesIO:
    bytes_data = str.encode(data)
    return BytesIO(bytes_data)
