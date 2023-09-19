import argparse
import psycopg2
import json


def connect_to_database(credentials_file):
    try:
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
            conn = psycopg2.connect(
                dbname=credentials['POSTGRES_DB'],
                user=credentials['POSTGRES_USER'],
                password=credentials['POSTGRES_PASSWORD'],
                host=credentials['POSTGRES_ADDRESS'],
                port=credentials['POSTGRES_PORT']
            )
            return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error executing query: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description="Execute a SELECT query on a PostgreSQL table.")
    parser.add_argument("--credentials",
                        required=False,
                        help="Path to the JSON credentials file",
                        default="credentials.json")
    parser.add_argument("--table",
                        required=True,
                        help="Name of the table to query")
    args = parser.parse_args()

    connection = connect_to_database(args.credentials)
    if connection:
        query = f"SELECT * FROM {args.table};"
        rows = execute_query(connection, query)
        if rows:
            print(f"Received {len(rows)} records")
        connection.close()


if __name__ == "__main__":
    main()
