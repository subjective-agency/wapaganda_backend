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
    def _import_table_data(json_filename):
        """
        Import data from JSON file to Postgres table
        """
        table_name = os.path.splitext(os.path.basename(json_filename))[0]
        try:
            with open(json_filename, "r") as json_file:
                data = json.load(json_file)

            cursor = self.connection.cursor()

            for record in data:
                placeholders = ', '.join(['%s'] * len(record))
                columns = ', '.join(record.keys())
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                values = list(record.values())

                cursor.execute(query, values)
                self.connection.commit()

            logger.info(f"Data imported from {json_filename} to {table_name}")
        except Exception as e:
            logger.error(f"Error importing data from {json_filename} to {table_name}: {e}")
            self.connection.rollback()

    def import_tables(self, json_files):
        """
        Import data from JSON files to Postgres database
        """
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
