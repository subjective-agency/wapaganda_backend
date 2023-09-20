import os


def read_table_names(table_names_file):
    """
    Read table names from file, skipping empty lines
    """
    table_names = []
    if table_names_file is not None:
        with open(table_names_file, "r") as file:
            table_names = [line.strip() for line in file if line.strip()]
    return table_names


def rename_json_files(export_dir):
    """
    List all JSON files with names matching *_batch_0.json and rename to add leading zeros
    """
    if not os.path.isdir(export_dir):
        print(f"No directory {export_dir} found")
        return

    json_files = [file for file in os.listdir(export_dir) if "_batch_" in file and file.endswith(".json")]
    if not json_files:
        print("No matching JSON files found")
        return
    print(f"Found following batches: {json_files}")

    max_batch_index = -1

    # Calculate the maximum batch index from the existing filenames
    for json_file in json_files:
        parts = json_file.split("_batch_")
        if len(parts) == 2:
            try:
                batch_index = int(parts[1].split(".json")[0])
                max_batch_index = max(max_batch_index, batch_index)
            except ValueError:
                pass

    if max_batch_index == -1:
        print("No valid batch indexes found in JSON filenames")
        return

    # Determine the number of leading zeros required
    num_leading_zeros = len(str(max_batch_index))

    # Rename the files with leading zeros
    for json_file in json_files:
        parts = json_file.split("_batch_")
        if len(parts) == 2:
            try:
                batch_index = int(parts[1].split(".json")[0])
                new_batch_index = str(batch_index).zfill(num_leading_zeros)
                new_file_name = f"{parts[0]}_batch_{new_batch_index}.json"
                os.rename(os.path.join(export_dir, json_file), os.path.join(export_dir, new_file_name))
                print(f"{json_file} -> {new_file_name}")
            except ValueError:
                pass
