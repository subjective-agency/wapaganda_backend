import os.path
import psycopg2
from supaword.log_helper import logger
from tools.postgres_table import PostgresTable

__doc__ = """Export data from Postgres database to JSON files
We utilize the class from standard Django manage.py script
"""


class PostgresDbExport:

    # noinspection PyUnresolvedReferences
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
        self.export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'export')
        if not os.path.exists(self.export_dir):
            logger.info(f"Creating export directory {self.export_dir}")
            os.makedirs(self.export_dir)

    def get_table(self, table_name, restore):
        """
        Get a PostgresTable instance for a specific table.
        :param table_name: The name of the table to export.
        :param restore: Whether to pick up export process
        :return: PostgresTable instance.
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return PostgresTable(self.connection, table_name, self.export_dir, 100000, restore)
        except Exception as e:
            logger.error(f"Error get_table(): {e}")

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()

    def export_to_json(self, table_names: list, restore: bool):
        """
        Export data from Postgres database to JSON files.
        :param table_names: List of table names to export.
        :param restore: Whether to pick up previous export
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
                table = self.get_table(table_name, restore)
                if restore is False:
                    table.remove_existing_files()
                table.export_table()
        except Exception as e:
            logger.error(f"Error export_to_json(): {e}")
        finally:
            if self.connection:
                self.connection.close()
