import os.path
import psycopg2
import json
from supaword.log_helper import logger
from datetime import datetime, date

__doc__ = """Export data from Postgres database to JSON files
We utilize the class from standard Django manage.py script
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


class PostgresDbExport:

    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        """
        Initialize database connection and do basic validation
        """
        assert len(dbname) > 0, "Database name is empty"
        assert len(user) > 0, "Database username is empty"
        assert len(password) > 0, "Database password is empty"
        assert len(host) > 0, "Database host is empty"
        assert port > 0, "Database port is empty"
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "export")
        if not os.path.exists(self.export_dir):
            logger.info(f"Creating export directory {self.export_dir}")
            os.makedirs(self.export_dir)

    @staticmethod
    def _serialize_datetime(obj):
        """
        Serialize datetime and date objects to ISO format
        Convert other types to string
        """
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return str(obj)

    def _get_column_data_types(self, table_name) -> dict:
        """
        Get column names and data types for a given table
        :param table_name:
        :return: dict of column names and data types
        """
        query = f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (table_name,))
            column_data_types = {row[0]: row[1] for row in cursor.fetchall()}
        logger.info(f"Column data types for table {table_name}: {column_data_types}")
        return column_data_types

    @staticmethod
    def _serialize_record(cursor, record, column_data_types):
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

    def _export_table(self, table_name, rewrite=True):
        """
        Export a single table to a JSON file
        """
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {table_name}"

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            column_data_types = self._get_column_data_types(table_name)
            serialized_records = [self._serialize_record(cursor, record, column_data_types) for record in rows]

            json_filename = os.path.join(self.export_dir, f"{table_name}.json")

            # Check if the JSON file already exists
            if rewrite and os.path.exists(json_filename):
                logger.warning(f"Warning: JSON file {json_filename} already exists and will be overwritten")
            elif rewrite:
                logger.warning(f"Warning: JSON file {json_filename} already exists; exiting")
                return

            with open(json_filename, "w", encoding="utf-8") as json_file:
                logger.info(f"Exporting table {table_name} to {json_filename}")
                json.dump(serialized_records, json_file, cls=CustomJSONEncoder, ensure_ascii=False, indent=2)
            logger.info(f"Table {table_name} exported to {json_filename}")
        except Exception as e:
            logger.error(f"Error exporting table {table_name}: {e}")
        finally:
            cursor.close()

    def export_to_json(self, table_names: list, rewrite: bool):
        """
        Export data from Postgres database to JSON files
        :param table_names:
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            for table_name in table_names:
                self._export_table(table_name, rewrite)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            if self.connection:
                self.connection.close()
