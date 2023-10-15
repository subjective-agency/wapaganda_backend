import os.path
import psycopg2
import json
from supaword.log_helper import logger
from datetime import datetime, date

__doc__ = """
"""


class PostgresDbCleanup:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def drop_tables(self, table_names):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            cursor = self.connection.cursor()
            drop_command = f"DROP TABLE IF EXISTS {', '.join(table_names)} CASCADE"
            cursor.execute(drop_command)
            self.connection.commit()

            for table_name in table_names:
                logger.info(f"Table {table_name} dropped")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            if self.connection:
                self.connection.close()

    def _truncate_table(self, table_name):
        try:
            cursor = self.connection.cursor()
            truncate_command = f"TRUNCATE TABLE {table_name} CASCADE"
            cursor.execute(truncate_command)
            self.connection.commit()
            logger.info(f"Table {table_name} truncated")
        except Exception as e:
            logger.error(f"Error truncating table {table_name}: {e}")
            self.connection.rollback()

    def truncate_tables(self, table_names):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            for table_name in table_names:
                self._truncate_table(table_name)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            if self.connection:
                self.connection.close()

