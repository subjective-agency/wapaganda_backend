import json
import os.path

from supaword.log_helper import logger
from datetime import datetime, date


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


class PostgresTable:
    """
    Abstraction of PostgresTable in context of table export
    """

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

    def __init__(self, connection, table_name, export_dir, batch_size, rewrite=False, restore=False):
        """
        Initialize a PostgresTable instance.
        :param connection: An existing PostgresSQL database connection.
        :param table_name: The name of the table to export (including schema if explicitly specified).
        :param export_dir: The directory where JSON files will be exported.
        :param batch_size: Number of records to export in each batch.
        :param rewrite: If True, rewrite already exported tables
        :param restore: If True, resume exporting from the last completed batch.
        """
        self.connection = connection
        if not table_name:
            raise RuntimeError("Empty table name")
        if '.' in table_name:
            self.schema_name, self.table_name = table_name.split('.')
        else:
            self.schema_name, self.table_name = 'public', table_name
        self.fully_qualified_name = f"{self.schema_name}.{self.table_name}"
        self.export_dir = os.path.abspath(export_dir)
        self.batch_size = batch_size
        self.total_rows = None
        self.restore = restore
        self.rewrite = rewrite
        logger.info(f"Create PostgresTable {self.schema_name}.{self.table_name} with batch_size {batch_size}")

    # noinspection SqlResolve
    def _get_column_data_types(self) -> dict:
        """
        Get column names and data types for a given table.
        :return: dict of column names and data types
        """
        query = """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
            AND table_schema = %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.table_name, self.schema_name))
            column_data_types = {row[0]: row[1] for row in cursor.fetchall()}
        logger.info(f"Column data types for table {self.schema_name}.{self.table_name}: {column_data_types}")
        return column_data_types

    # noinspection SqlResolve
    def _count_rows(self):
        """
        Count the number of rows in the table using SELECT COUNT(*).
        """
        query = f"SELECT COUNT(*) FROM {self.fully_qualified_name}"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            row_count = cursor.fetchone()[0]
        return row_count

    def get_count(self):
        """
        :return:
        """
        if self.total_rows is None:
            self.total_rows = self._count_rows()
        return self.total_rows

    def export_table(self):
        """
        Export data from the table to JSON files.
        """
        logger.info(f"Table {self.fully_qualified_name} has {self.get_count()} records")
        if self.get_count() > self.batch_size:
            logger.info("Export in batches")
            self._export_batches()
        else:
            logger.info("Export as a single table")
            self._export_table()

    # noinspection SqlResolve
    def _export_table(self):
        """
        Export a single table to a JSON file
        """
        cursor = self.connection.cursor()
        query = f"""SELECT * FROM {self.schema_name}.{self.table_name}"""
        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            column_data_types = self._get_column_data_types()
            serialized_records = [
                PostgresExportHelper.serialize_record(cursor, record, column_data_types) for record in rows
            ]
            logger.info(f"Got {len(serialized_records)} records from table {self.fully_qualified_name}")

            json_filename = os.path.join(self.export_dir, f"{self.fully_qualified_name}.json")

            # Check if the file already exists and self.rewrite is False
            if not self.rewrite and os.path.exists(json_filename) and os.path.getsize(json_filename) > 0:
                logger.warning(
                    f"Table {self.fully_qualified_name} already exists in {json_filename}. Use --rewrite to overwrite.")
                return

            with open(json_filename, "w", encoding="utf-8") as json_file:
                logger.info(f"Exporting table {self.fully_qualified_name} to {json_filename}")
                json.dump(serialized_records, json_file, cls=self.CustomJSONEncoder, ensure_ascii=False, indent=2)
            logger.info(f"Table {self.fully_qualified_name} exported to {json_filename}")
        except Exception as e:
            logger.error(f"Error exporting table {self.fully_qualified_name}: {e}")
        finally:
            cursor.close()

    def _split_table(self):
        """
        Split a table into equal batches based on the given batch size
        Calculate the number of batches needed
        """
        total_rows = self.get_count()
        num_batches = (total_rows + self.batch_size - 1) // self.batch_size
        batches = [(self.batch_size, i * self.batch_size) for i in range(num_batches)]
        logger.info(f"Split export into {num_batches} batches: {batches}")
        return batches

    def _last_completed_batch(self, json_filename_base):
        """
        Find the last completed batch.
        """
        max_batch_num = len(self._split_table()) - 1
        num_leading_zeros = len(str(max_batch_num))

        last_completed_batch = -1
        for batch_num in range(max_batch_num + 1):
            batch_index_str = str(batch_num).zfill(num_leading_zeros)
            batch_filename = f"{json_filename_base}{batch_index_str}.json"
            if os.path.exists(batch_filename) and os.path.getsize(batch_filename) > 0:
                last_completed_batch = batch_num

        return last_completed_batch

    def _export_batches(self):
        """
        Export a single table to multiple JSON files in equal-sized batches
        """
        cursor = self.connection.cursor()
        logger.info(f"Export batches: rewrite={self.rewrite}")
        logger.info(f"Export batches: restore={self.restore}")
        try:
            column_data_types = self._get_column_data_types()
            json_filename_base = os.path.join(self.export_dir, f"{self.fully_qualified_name}_batch_")

            # Remove existing batch files if self.rewrite is True
            if self.rewrite:
                self._remove_batch_files(json_filename_base)

            # Find the last completed batch if restore flag is set
            if self.restore:
                last_completed_batch = self._last_completed_batch(json_filename_base)

                if last_completed_batch >= 0:
                    logger.info(f"Resuming export from Batch {last_completed_batch + 1}")
                    batch_ranges = self._split_table()[last_completed_batch + 1:]
                else:
                    batch_ranges = self._split_table()
            else:
                batch_ranges = self._split_table()

            # Calculate the number of leading zeros needed based on the total number of batches
            max_batch_num = len(batch_ranges) - 1
            num_leading_zeros = len(str(max_batch_num))

            for batch_num, (limit, offset) in enumerate(batch_ranges):
                batch_query = f"SELECT * FROM {self.fully_qualified_name} LIMIT %s OFFSET %s"
                cursor.execute(batch_query, (limit, offset))
                rows = cursor.fetchall()
                serialized_records = [
                    PostgresExportHelper.serialize_record(cursor, record, column_data_types) for record in rows
                ]

                # Add leading zeros to the batch index
                batch_index_str = str(batch_num).zfill(num_leading_zeros)
                batch_filename = f"{json_filename_base}{batch_index_str}.json"

                with open(batch_filename, "w", encoding="utf-8") as json_file:
                    logger.info(
                        f"Exporting table {self.fully_qualified_name} (Batch {batch_index_str}) to {batch_filename}")
                    json.dump(serialized_records, json_file, cls=self.CustomJSONEncoder, ensure_ascii=False, indent=2)
                logger.info(f"Table {self.fully_qualified_name} (Batch {batch_index_str}) exported to {batch_filename}")
        except Exception as e:
            logger.error(f"Error exporting table {self.fully_qualified_name}: {e}")
        finally:
            cursor.close()

    def _remove_batch_files(self, json_filename_base):
        """
        Remove existing batch files.
        """
        logger.info(f"Removing batch files for {json_filename_base} table")
        max_batch_num = len(self._split_table()) - 1
        num_leading_zeros = len(str(max_batch_num))

        for batch_num in range(max_batch_num + 1):
            batch_index_str = str(batch_num).zfill(num_leading_zeros)
            batch_filename = f"{json_filename_base}{batch_index_str}.json"
            if os.path.exists(batch_filename):
                os.remove(batch_filename)
                
    def remove_existing_files(self):
        """
        Remove existing JSON files for the table if they exist
        """
        json_filename = os.path.join(self.export_dir, f"{self.fully_qualified_name}.json")
        if os.path.exists(json_filename):
            os.remove(json_filename)

        batch_files = [f for f in os.listdir(self.export_dir) if f.startswith(f"{self.fully_qualified_name}_batch_")]
        logger.info(f"Prepare to remove {len(batch_files)} files")
        for batch_file in batch_files:
            batch_filename = os.path.join(self.export_dir, batch_file)
            if os.path.exists(batch_filename):
                os.remove(batch_filename)
