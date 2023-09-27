import psycopg2

class ValidateTable:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
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
        try:
            self.connection = psycopg2.connect(**self.db_params)
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)
            exit()

    def validate_table(self, table_name):
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
        self.cursor.close()
        self.connection.close()

# Example usage:
# validator = ValidateTable("your_db_name", "your_db_user", "your_db_password", "your_db_host", your_db_port)
# validator.connect_to_database()
# validator.validate_table("theory")
# validator.close_connection()
