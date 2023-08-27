import os.path

import psycopg2
import json
from supaword.log_helper import logger
from datetime import datetime, date

TABLE_NAMES = [
    "days_of_war",
    "komso_episodes",
    "media_coverage_type",
    "media_roles",
    "media_segments",
    "msegments_to_rchannels_mapping",
    "msegments_to_ychannels_mapping",
    "ntv_episodes",
    "organization_type",
    "organizations",
    "people",
    "people_3rdprt_details_raw",
    "people_bundles",
    "people_extended",
    "people_in_bundles",
    "people_in_orgs",
    "people_in_ur",
    "people_on_photos",
    "people_on_smotrim",
    "people_on_youtube",
    "people_to_msegments_mapping",
    "photos",
    "printed",
    "printed_to_people_mapping",
    "quotes",
    "rutube_channels",
    "rutube_vids",
    "smotrim_episodes",
    "telegram_authors",
    "telegram_channels",
    "theory",
    "websites",
    "youtube_authors",
    "youtube_channels",
    "youtube_vids"
]


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return super().default(obj)


class PostgresDbExport:
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
        self.export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "export")
        if not os.path.exists(self.export_dir):
            logger.info(f"Creating export directory {self.export_dir}")
            os.makedirs(self.export_dir)

    @staticmethod
    def _serialize_datetime(obj):
        """
        Serialize datetime and date objects to ISO format
        Convert other types to string
        """
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return str(obj)

    def _get_column_data_types(self, table_name):
        query = f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (table_name,))
            column_data_types = {row[0]: row[1] for row in cursor.fetchall()}
        logger.info(f"Column data types for table {table_name}: {column_data_types}")
        return column_data_types

    def _serialize_record(self, cursor, record, column_data_types):
        description = [desc[0] for desc in cursor.description]
        serialized_record = {}

        for field, value, data_type in zip(description, record, column_data_types.values()):
            try:
                if value is None:
                    serialized_record[field] = None
                elif data_type == "timestamp" and isinstance(value, (datetime, date)):
                    serialized_record[field] = value
                elif data_type == "boolean":
                    serialized_record[field] = value
                elif data_type == "integer":
                    serialized_record[field] = value
                elif data_type in ("json", "jsonb"):
                    # Don't parse JSON values, assign them directly
                    serialized_record[field] = value
                elif data_type == "array":
                    serialized_record[field] = json.loads(value.replace("'", "\""))
                else:
                    serialized_record[field] = value
            except Exception as e:
                logger.error(f"Error serializing field '{field}' with value '{value}' of data type '{data_type}': {e}")
                raise e

        return serialized_record

    def _export_table(self, table_name):
        """
        Export a single table to JSON file
        """
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {table_name}"

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            column_data_types = self._get_column_data_types(table_name)
            serialized_records = [self._serialize_record(cursor, record, column_data_types) for record in rows]

            json_filename = os.path.join(self.export_dir, f"{table_name}.json")
            with open(json_filename, "w", encoding="utf-8") as json_file:
                logger.info(f"Exporting table {table_name} to {json_filename}")
                json.dump(serialized_records, json_file, cls=CustomJSONEncoder, ensure_ascii=False, indent=2)
            logger.info(f"Table {table_name} exported to {json_filename}")
        except Exception as e:
            logger.error(f"Error exporting table {table_name}: {e}")
        finally:
            cursor.close()

    def export_to_json(self, table_names: list):
        """
        Export data from Postgres database to JSON files
        :param table_names:
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
                self._export_table(table_name)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            if self.connection:
                self.connection.close()


def export_table_names_to_text_file(table_names, file_path):
    with open(file_path, "w") as file:
        for table_name in table_names:
            file.write(table_name + "\n")


if __name__ == "__main__":
    text_file_path = "table_names.txt"
    export_table_names_to_text_file(TABLE_NAMES, text_file_path)
    print(f"Table names exported to {text_file_path}")