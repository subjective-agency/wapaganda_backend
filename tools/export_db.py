import time
import os.path
import psycopg2
from supaword.log_helper import logger
from tools.postgres_table import PostgresTableExport

__doc__ = """Export data from Postgres database to JSON files
We utilize the class from standard Django manage.py script
"""


class PostgresDbExport:
    BATCH_SIZE = 100000

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

    def create_connection(self):
        """
        Create a database connection.
        """
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()

    def get_table(self, table_name, rewrite, restore):
        """
        Get a PostgresTable instance for a specific table.
        :param table_name: The name of the table to export.
        :param restore: Whether to pick up export process
        :param rewrite: Whether to rewrite tables
        :return: PostgresTable instance
        """
        if self.connection is None:
            self.create_connection()
        return PostgresTableExport(connection=self.connection, table_name=table_name, export_dir=self.export_dir,
                                   batch_size=self.BATCH_SIZE, rewrite=rewrite, restore=restore, skip_export=False)

    def export_to_json(self, table_names: list, rewrite: bool, restore: bool):
        """
        Export data from Postgres database to JSON files.
        :param rewrite: Whether to rewrite exported JSON
        :param table_names: List of table names to export.
        :param restore: Whether to pick up previous export
        """
        for table_name in table_names:
            while True:
                try:
                    self.create_connection()
                    table = self.get_table(table_name=table_name, rewrite=rewrite, restore=restore)
                    table.export_table()
                    # Success, break out of the retry loop
                    break
                except psycopg2.OperationalError as e:
                    logger.error(f"Error exporting {table_name}: {e}")

                    # check if the exception indicates a timeout
                    self.close_connection()
                    if "timeout" in str(e).lower():
                        logger.info("Timeout exception, retrying in 60 seconds...")
                        time.sleep(60)
                    else:
                        # Break out of the retry loop for other exceptions
                        break
