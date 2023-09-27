import psycopg2


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
            "theory": f"""
                UPDATE theory
                SET original_content_metadata = original_content_metadata
                WHERE publish_date IS NOT NULL;
            """
            # Add more tables and their corresponding queries here
        }

    def connect_to_database(self):
        """
        Connects to the database
        """
        try:
            self.connection = psycopg2.connect(**self.db_params)
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)
            exit()

    def validate_table(self, table_name):
        """
        Executes the validation trigger for the given table
        """
        try:
            sql_query = self.query_dict.get(table_name)
            if sql_query:
                self.cursor.execute(sql_query)
                self.connection.commit()
                print(f"Validation trigger executed for table: {table_name}")
            else:
                print(f"No validation query found for table: {table_name}")
        except psycopg2.Error as e:
            print(f"Error executing validation trigger for table {table_name}:", e)

    def close_connection(self):
        """
        Closes the connection to the database
        """
        self.cursor.close()
        self.connection.close()
