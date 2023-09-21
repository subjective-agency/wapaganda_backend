import os
import json
from datetime import datetime, date
from supaword.log_helper import logger


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

    class CustomJSONEncoder(json.JSONEncoder):
        """
        Custom JSON encoder to serialize objects to ISO format
        """

        def default(self, obj):
            """
            Serialize datetime and date objects to ISO format
            """
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            if isinstance(obj, bytes):
                return obj.decode('utf-8')
            return super().default(obj)


class CustomJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to serialize objects to ISO format
    """

    def default(self, obj):
        """
        Serialize datetime and date objects to ISO format
        """
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return super().default(obj)


class PostgresExportHelper:

    @staticmethod
    def serialize_datetime(obj):
        """
        Serialize datetime and date objects to ISO format
        Convert other types to string
        """
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return str(obj)

    @staticmethod
    def serialize_record(cursor, record, column_data_types):
        """
        :param cursor:
        :param record:
        :param column_data_types:
        :return:
        """
        description = [desc[0] for desc in cursor.description]
        serialized_record = {}

        for field, value, data_type in zip(description, record, column_data_types.values()):
            try:
                if value is None:
                    serialized_record[field] = None
                elif data_type == "timestamp" and isinstance(value, (datetime, date)):
                    serialized_record[field] = value
                elif data_type == "boolean":
                    serialized_record[field] = value
                elif data_type == "integer":
                    serialized_record[field] = value
                elif data_type in ("json", "jsonb"):
                    # Don't parse JSON values, assign them directly
                    serialized_record[field] = value
                elif data_type == "array":
                    serialized_record[field] = json.loads(value.replace("'", "\""))
                else:
                    serialized_record[field] = value
            except Exception as e:
                logger.error(f"Error serializing field '{field}' with value '{value}' of data type '{data_type}': {e}")
                raise e

        return serialized_record
