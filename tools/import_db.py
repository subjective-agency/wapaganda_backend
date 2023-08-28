import os.path
import psycopg2
import json
from supaword.log_helper import logger
from datetime import datetime, date

__doc__ = """Import data from JSON files to Postgres database
We utilize the class from standard Django manage.py script
"""


class PostgresDbImport:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    @staticmethod
    def _serialize_value(value):
        """
        Convert dict or list to string representation
        """
        if isinstance(value, (dict, list)):
            return json.dumps(value)
        return value

    def _import_table_data(self, json_filename):
        """
        Import data from JSON file to Postgres table
        """
        table_name = os.path.splitext(os.path.basename(json_filename))[0]
        try:
            with open(json_filename, "r") as json_file:
                data = json.load(json_file)

            cursor = self.connection.cursor()

            logger.info(f"Importing data from {json_filename} to {table_name}")
            for index, record in enumerate(data, start=1):
                placeholders = ', '.join(['%s'] * len(record))
                columns = ', '.join(record.keys())
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                values = [self._serialize_value(value) for value in record.values()]

                try:
                    cursor.execute(query, values)
                    self.connection.commit()
                    logger.debug(f"Record {index} imported from {json_filename} to {table_name}")
                except Exception as e:
                    logger.error(f"Error importing record {index} from {json_filename} to {table_name}: {e}")
                    self.connection.rollback()
                    raise e

        except Exception as e:
            logger.error(f"Error loading data from {json_filename}: {e}")
            return

    def import_tables(self, table_names):
        """
        Import data from JSON files to Postgres database
        """
        json_files = [
            os.path.join(os.path.abspath("tools/import"), f"{table_name}.json") for table_name in table_names
        ]
        logger.info(f"Importing data from JSON files: {json_files}")
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            for json_filename in json_files:
                self._import_table_data(json_filename)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            if self.connection:
                self.connection.close()
