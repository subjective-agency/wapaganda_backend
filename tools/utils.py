def read_table_names(table_names_file):
    """
    Read table names from file
    """
    table_names = []
    if table_names_file is not None:
        with open(table_names_file, "r") as file:
            [table_names.append(line.strip()) for line in file.readlines()]
    return table_names
