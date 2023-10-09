import json
import time
import math
from datetime import datetime
import os.path
from collections import OrderedDict
from supaword.log_helper import logger
from tools.utils import CustomJSONEncoder, PostgresExportHelper


# noinspection SqlNoDataSourceInspection,SqlResolve
class PostgresTableExport:
    """
    Abstraction of PostgresTable in context of table export
    """

    def __init__(self, connection, table_name, export_dir, batch_size, rewrite, restore, skip_export):
        """
        Initialize a PostgresTable instance.
        :param connection: An existing PostgresSQL database connection.
        :param table_name: The name of the table to export (including schema if explicitly specified).
        :param export_dir: The directory where JSON files will be exported.
        :param batch_size: Number of records to export in each batch.
        :param rewrite: If True, rewrite already exported tables
        :param restore: If True, resume exporting from the last completed batch
        :param skip_export: If True, skip exporting the table if it is up-to-date
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
        self.rewrite = rewrite
        self.restore = restore
        self.skip_export = skip_export

        # OrderedDict of batch information dicts batch_num = {size, offset, filename}
        self.batches = OrderedDict()

        # Get from PSQL table
        self.total_rows = None

        # Get from PSQL information_schema.columns
        self.id_column_exists = False

        # Get from PSQL table information_schema.columns
        self.column_data_types = None

        # e.g. 'export/data.telegram_messages_'
        self.json_filename_base = None

        # If exporting in batches, should be enough leading zeros to cover the number of batches
        self.num_leading_zeros = 0

        # If table has enough records to export in batches
        self.is_batches = False

        # If table is up-to-date, we can skip export
        self.up_to_date = False

        self._preprocess()
        logger.info(f"Create PostgresTable {self.schema_name}.{self.table_name} with batch_size {batch_size}")

    def _preprocess(self):
        """
        Preprocess information about the table before exporting.
        What we actually do:
        - check if table has 'id' column
        - get column data types
        - check if table has enough records to export in batches
        - get last completed batch
        - check if table is up-to-date and we can skip export
        """
        # Check if the table is up-to-date and we can skip export
        if not self.rewrite and self.skip_export:
            last_data_timestamp = self._last_data_timestamp()
            if last_data_timestamp:
                logger.info(f"Last data timestamp for table {self.fully_qualified_name}: {last_data_timestamp}")

            last_edited = self._last_edited()
            if last_edited:
                logger.info(f"Last edited timestamp for table {self.fully_qualified_name}: {last_edited}")

            if last_data_timestamp and last_edited and last_data_timestamp == last_edited:
                logger.info(f"Table {self.fully_qualified_name} is up to date. No export required")
                self.up_to_date = True
                return

        # Check if the table has an 'id' column to sort by
        self.id_column_exists = self._check_id_column_exists()
        if self.id_column_exists:
            logger.info(f"Table {self.fully_qualified_name} has an 'id' column")

        self.column_data_types = self._get_column_data_types()

        # Check if the table has enough records to export in batches
        if self.get_count() > self.batch_size:
            self.is_batches = True
            logger.info(f"Table {self.fully_qualified_name} has enough records to export in batches")

            batches_dir = os.path.join(self.export_dir, self.fully_qualified_name)
            os.makedirs(batches_dir, exist_ok=True)
            logger.info(f"Batches directory for {self.fully_qualified_name}: {batches_dir}")

            self.json_filename_base = os.path.join(batches_dir, f"{self.fully_qualified_name}_batch_")
            logger.info(f"JSON filename base for {self.fully_qualified_name}: {self.json_filename_base}")

            self.batches = self._split_table()
            logger.info(f"Number of batches for {self.fully_qualified_name}: {len(self.batches)}")

            # Calculate the number of leading zeros needed for batch filenames
            num_batches = len(self.batches)
            self.num_leading_zeros = int(math.ceil(math.log10(num_batches + 1)))
            logger.info(
                f"{num_batches} batches; {num_digits} digits; {self.num_leading_zeros} leading zeros"
            )

        # Check if we need to restore from the last completed batch
        logger.debug(f"self.restore={self.restore} self.is_batches={self.is_batches}")
        if self.restore and self.is_batches:
            table_dir = os.path.join(self.export_dir, self.fully_qualified_name)
            logger.info(f"Table directory for {self.fully_qualified_name}: {table_dir}")

            self.last_completed_batch = self._last_completed_batch()
            logger.info(f"Last completed batch for {self.fully_qualified_name}: {self.last_completed_batch}")

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

    def _count_rows(self):
        """
        Count the number of rows in the table using SELECT COUNT(*).
        """
        query = f"SELECT COUNT(*) FROM {self.fully_qualified_name}"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            row_count = cursor.fetchone()[0]
        return row_count

    def _last_edited(self):
        """
        Get the timestamp of the last change to the table.
        """
        query = """
            SELECT last_analyze
            FROM pg_stat_all_tables
            WHERE schemaname = %s AND relname = %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.schema_name, self.table_name))
            result = cursor.fetchone()
            logger.info(f"Table {self.schema_name}.{self.table_name} last edited {result}")
            if result is not None and result[0] is not None:
                return datetime.fromisoformat(result[0])
        return None

    def _last_data_timestamp(self):
        """
        Find the latest 'added_on', 'added_at', or 'created_at' timestamp in specific JSON data files.
        """
        # Define the JSON schema field names to check
        timestamp_fields = ['added_on', 'added_at', 'created_at']

        # Initialize the latest timestamp as None
        latest_timestamp = None

        # List of JSON filenames to check
        json_filenames = []

        if self.is_batches:
            # If exporting in batches, generate a list of batch JSON filenames
            for batch_num in range(self.batch_count):
                batch_index_str = f"{batch_num:0{self.num_leading_zeros}d}"
                json_filenames.append(f"{self.json_filename_base}{batch_index_str}.json")
        else:
            # If exporting as a single table, use the main JSON filename
            json_filenames.append(f"{self.fully_qualified_name}.json")

        # Directory where JSON data files are located
        data_dir = os.path.join(self.export_dir, self.fully_qualified_name)

        # Iterate through specified JSON data files
        for filename in json_filenames:
            file_path = os.path.join(data_dir, filename)
            if not os.path.isfile(file_path):
                continue
            with open(file_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                for record in data:
                    for field in timestamp_fields:
                        if field in record and record[field]:
                            timestamp = datetime.fromisoformat(record[field])
                            if latest_timestamp is None or timestamp > latest_timestamp:
                                latest_timestamp = timestamp

        return latest_timestamp

    def _export_table(self):
        """
        Export a single table to a JSON file
        """
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {self.schema_name}.{self.table_name}"
        if self._check_id_column_exists():
            query += " ORDER BY id"

            cursor.execute(query)
            rows = cursor.fetchall()

            serialized_records = [
                PostgresExportHelper.serialize_record(cursor, record, self.column_data_types) for record in rows
            ]
            logger.info(f"Got {len(serialized_records)} records from table {self.fully_qualified_name}")

            # Check if the file already exists and self.rewrite is False
            json_filename = os.path.join(self.export_dir, f"{self.fully_qualified_name}.json")

            if not self.rewrite and os.path.exists(json_filename) and os.path.getsize(json_filename) > 0:
                logger.warning(
                    f"Table {self.fully_qualified_name} already exists in {json_filename}; use --rewrite to overwrite.")
                return

            with open(json_filename, "w", encoding="utf-8") as json_file:
                logger.info(f"Exporting table {self.fully_qualified_name} to {json_filename}")
                json.dump(serialized_records, json_file, cls=CustomJSONEncoder, ensure_ascii=False, indent=2)
            logger.info(f"Table {self.fully_qualified_name} exported to {json_filename}")
            cursor.close()

    def _split_table(self):
        """
        Split a table into equal batches based on the given batch size
        Calculate the number of batches needed
        """
        total_rows = self.get_count()
        num_batches = total_rows // self.batch_size
        remainder = total_rows % self.batch_size

        if remainder > 0:
            num_batches += 1

        batches = OrderedDict()
        for i in range(num_batches):
            batch_index = i + 1
            last_batch_index = num_batches - 1
            batches[batch_index] = {
                "batch_num": i + 1,
                "batch_size": self.batch_size if i != last_batch_index else remainder,
                "offset": i * self.batch_size,
                "filename": self._get_batch_json_filename(batch_index)
            }

        logger.info(f"Split export into {num_batches} batches")
        logger.info(f"First batch {list(batches.values())[0]}")
        logger.info(f"Last batch {list(batches.values())[-1]}")
        return batches

    def _get_batch_json_filename(self, batch_number):
        """
        Get the full JSON filename for a batch based on batch number.
        """
        batch_index_str = str(batch_number).zfill(self.num_leading_zeros)
        result = f"{self.json_filename_base}{batch_index_str}.json"
        return result

    def _last_completed_batch(self):
        """
        Find the last completed batch.
        """
        last_completed_batch = -1
        for batch_num, batch_info in self.batches.items():
            batch_filename = batch_info["filename"]
            logger.debug(f"_last_completed_batch: {self.fully_qualified_name}:{batch_filename}")
            if os.path.exists(batch_filename) and os.path.getsize(batch_filename) > 0:
                logger.debug(f"Found batch {batch_num} for {self.fully_qualified_name}")
                last_completed_batch = batch_num

        return last_completed_batch

    def _remove_batch_files(self, table_dir):
        """
        Remove existing batch files.
        """
        logger.info(f"Removing batch files for {self.fully_qualified_name} table")
        max_batch_num = len(self._split_table()) - 1
        num_leading_zeros = len(str(max_batch_num))

        for batch_num in range(max_batch_num + 1):
            batch_index_str = str(batch_num).zfill(num_leading_zeros)
            batch_filename = os.path.join(table_dir, f"{self.fully_qualified_name}_batch_{batch_index_str}.json")
            if os.path.exists(batch_filename):
                os.remove(batch_filename)

    def _check_id_column_exists(self):
        """
        Check if the 'id' column exists in the table's metadata.
        """
        query = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s
            AND table_schema = %s
            AND column_name = 'id'
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.table_name, self.schema_name))
            return cursor.fetchone() is not None

    def _export_batches(self):
        """
        Export a single table to multiple JSON files in equal-sized batches.
        """
        if not self.is_batches:
            raise RuntimeError(f"Table {self.fully_qualified_name} does not have enough records to export in batches")

        cursor = self.connection.cursor()
        logger.info(f"Export batches: rewrite={self.rewrite}")
        logger.info(f"Export batches: restore={self.restore}")
        logger.info(f"Export batches: skip_export={self.skip_export}")

        if self.rewrite:
            self._remove_batch_files(table_dir=self.export_dir)

        if self.last_completed_batch > 0:
            logger.info(f"Resuming export from batch {self.last_completed_batch + 1} of {len(self.batches)}")

        for batch_num, batch_info in self.batches.items():
            batch_size = batch_info["batch_size"]
            offset = batch_info["offset"]
            filename = batch_info["filename"]
            if self.last_completed_batch > 0 and batch_num <= self.last_completed_batch:
                continue
            logger.info(f"Exporting batch {batch_num} of {len(self.batches)}: {filename}")
            self._export_batch(cursor=cursor, batch_num=batch_num, limit=batch_size, offset=offset, filename=filename)
        cursor.close()

    def _export_batch(self, cursor, batch_num, limit, offset, filename):
        """
        Export a single batch of table data to a JSON file
        :param cursor: A PostgresSQL database cursor
        :param batch_num: The batch number
        :param limit: The total number of records to export from the table
        :param offset: The number of records in the batch
        :param filename: The filename of the JSON batch to export to
        """
        start_time = time.time()
        batch_query = f"SELECT * FROM {self.fully_qualified_name}"
        if self.id_column_exists:
            batch_query += " ORDER BY id"
        batch_query += " LIMIT %s OFFSET %s"

        cursor.execute(batch_query, (limit, offset))
        rows = cursor.fetchall()
        serialized_records = [
            PostgresExportHelper.serialize_record(cursor, record, self.column_data_types) for record in rows
        ]

        with open(filename, "w", encoding="utf-8") as json_file:
            logger.info(f"Write exported file {filename}")
            json.dump(serialized_records, json_file, cls=CustomJSONEncoder, ensure_ascii=False, indent=2)

        end_time = time.time()
        transaction_duration = end_time - start_time
        logger.info(f"Batch {batch_num} exported to {filename} in {transaction_duration:.2f} seconds")

    def export_table(self):
        """
        Export data from the table to JSON files.
        """
        # Allow exiting early if the data is up-to-date
        if self.up_to_date:
            logger.info(f"Table {self.fully_qualified_name} export exiting early")
            return

        logger.info(f"Table {self.fully_qualified_name} has {self.get_count()} records")

        if self.get_count() > self.batch_size:
            logger.info("Export in batches")
            self._export_batches()
        else:
            logger.info("Export as a single table")
            self._export_table()

    def get_count(self):
        """
        :return:
        """
        if self.total_rows is None:
            self.total_rows = self._count_rows()
        return self.total_rows
