def calculate_number_of_rows(file: bytes):
    return len(file.decode("utf-8").splitlines())
