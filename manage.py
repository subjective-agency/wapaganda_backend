#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import urllib.request
from urllib.error import HTTPError
from supaword.secure_env import POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_USER, POSTGRES_DB
from tools.import_db import PostgresDbExport, TABLE_NAMES
from supaword.log_helper import logger
import zipfile
import io

URLS = [
    f'https://svfizyfozagyqkkjzqdc.supabase.co/storage/v1/object/public/packages/frontend/',
    f'https://wapaganda-frontend.s3.amazonaws.com/builds/'
]


def fetch_static(version):
    """
    Fetch static files from the given urls, unpack to static if successful
    """
    for url in URLS:
        archive_name = f'wapaganda-frontend-{version}.zip'
        archive_url = f'{url}{archive_name}'

        try:
            logger.info(f"Try fetching {archive_url}")
            response = urllib.request.urlopen(archive_url)

            if response.status == 200:
                logger.info(f"Extracting zip from {archive_url}")
                with zipfile.ZipFile(io.BytesIO(response.read())) as archive:
                    archive.extractall("static")
                extracted_files = os.listdir("static/build")
                extracted_to = os.path.abspath("static/build")
                logger.info(f"Successfully extracted to {extracted_to} following static files: {extracted_files}")
                return
            else:
                logger.info(f"Failed to fetch static files, trying the next. Status code: {response.status}")
                continue

        except HTTPError as e:
            logger.info(f"Failed to fetch static files, trying the next. Return code {e.code}")
            continue


def export_data(table_names_file=None):
    """
    Export data from Postgres database to JSON files
    """
    db_export = PostgresDbExport(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_ADDRESS,
        port=POSTGRES_PORT
    )
    # Read table names from file
    table_names = []
    if table_names_file is not None:
        with open(table_names_file, "r") as file:
            [table_names.append(line.strip()) for line in file.readlines() if line.strip() in TABLE_NAMES]
    if len(table_names) == 0:
        table_names = TABLE_NAMES
    db_export.export_to_json(table_names=table_names)


def main():
    """
    Run administrative tasks
    """
    command_handlers = {
        "fetchstatic": {
            "handle": fetch_static,
            "params": 1
        },
        "exportdata": {
            "handle": export_data,
            "params": 1
        }
    }

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supaword.settings')
    command = sys.argv[1] if len(sys.argv) > 1 else None
    if command in command_handlers:
        params_num = len(sys.argv) - 2
        if params_num == command_handlers[command]["params"]:
            logger.info(f"Executing command '{command}'")
            command_handlers[command]["handle"](*sys.argv[2:])
            return 0
        else:
            logger.error(f"Invalid number of parameters {params_num} for command '{command}'")
            return 1

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
