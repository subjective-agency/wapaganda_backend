import psycopg2
from wganda.log_helper import logger


# noinspection SqlNoDataSourceInspection,SqlResolve
class TableValidator:
    """
    This class is used to execute validation triggers on tables in the database.
    Almost every table features an 'id' column, which is used to identify the problem rows
    Example usage:
        validate_table = TableValidator("dbname", "user", "password", "host", 5432)
        validate_table.connect_to_database()
        validate_table.validate_table("theory")
        validate_table.close_connection()
    """

    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        """
        :param dbname:
        :param user:
        :param password:
        :param host:
        :param port:
        """
        self.connection = None
        self.cursor = None
        self.db_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.query_dict = {
            "theory": """
                UPDATE theory
                SET original_content_metadata = original_content_metadata
                WHERE id=%s AND publish_date IS NULL;
            """
            # Add more tables and their corresponding queries here
        }

    def connect_to_database(self):
        """
        Connects to the database
        """
        try:
            logger.info("Connecting to database")
            self.connection = psycopg2.connect(**self.db_params)
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            logger.error(f"Error connecting to database: {e}")
            exit()

    def validate_table(self, table_name):
        # Get the IDs of records that trigger an error during update
        self.cursor.execute(f"SELECT id FROM {table_name} WHERE publish_date IS NULL")
        record_ids = [row[0] for row in self.cursor.fetchall()]
        logger.info(f"Found {len(record_ids)} records to validate in {table_name}")

        for record_id in record_ids:
            try:
                sql_query = self.query_dict[table_name]
                self.cursor.execute(sql_query, (record_id,))
                self.connection.commit()
                logger.info(f"Validation trigger executed for {table_name}, ID: {record_id}")
            except psycopg2.Error as e:
                logger.error(f"Error executing validation for {table_name}, ID: {record_id}, Error: {e}")
                self.connection.rollback()

    def close_connection(self):
        """
        Closes the connection to the database
        """
        logger.info("Closing database connection")
        self.cursor.close()
        self.connection.close()
