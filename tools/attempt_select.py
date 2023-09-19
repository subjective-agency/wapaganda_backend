import argparse
import psycopg2
import json


def connect_to_database(credentials_file):
    try:
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
            conn = psycopg2.connect(
                dbname=credentials['dbname'],
                user=credentials['user'],
                password=credentials['password'],
                host=credentials['host'],
                port=credentials['port']
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
    parser.add_argument("--credentials", required=True, help="Path to the JSON credentials file.")
    parser.add_argument("--table", required=True, help="Name of the table to query.")
    args = parser.parse_args()

    connection = connect_to_database(args.credentials)
    if connection:
        query = f"SELECT * FROM {args.table};"
        rows = execute_query(connection, query)

        if rows:
            print("Query results:")
            for row in rows:
                print(row)
        
        connection.close()


if __name__ == "__main__":
    main()
