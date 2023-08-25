import os.path

import psycopg2
import json
from supaword.log_helper import logger


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
        self.export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "export")
        if not os.path.exists(self.export_dir):
            logger.info(f"Creating export directory {self.export_dir}")
            os.makedirs(self.export_dir)

    def _export_table(self, connection, table_name):
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name}"

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            json_filename = os.path.join(self.export_dir, f"{table_name}.json")
            with open(json_filename, "w") as json_file:
                logger.info(f"Exporting table {table_name} to {json_filename}")
                json.dump(rows, json_file)
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
        connection = None
        try:
            connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            for table_name in table_names:
                self._export_table(connection, table_name)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            if connection:
                connection.close()
