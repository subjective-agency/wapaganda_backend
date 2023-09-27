import psycopg2
import os

class ValidateTheoryTable:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        self.db_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file_path = os.path.join(self.script_dir, "error_log.txt")

    def connect_to_database(self):
        try:
            self.connection = psycopg2.connect(**self.db_params)
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)
            exit()

    def validate_metadata_dates(self):
        try:
            self.cursor.execute("""
                SELECT id, original_content_metadata->>'date'
                FROM theory
                WHERE original_content_metadata->>'date' ~ '\d{4}-\d{2}-\d{2}'
            """)
            
            with open(self.log_file_path, "a") as log_file:
                for row in self.cursor.fetchall():
                    theory_id, date_str = row
                    try:
                        # Attempt to parse the date; if it fails, log the error to the file
                        error_message = f"Date inconsistency for theory ID {theory_id}: {date_str}\n"
                        log_file.write(error_message)
                    except Exception as e:
                        print(f"Error logging error to file: {e}")

        except psycopg2.Error as e:
            print("Error querying the database:", e)

        finally:
            self.cursor.close()
            self.connection.close()
