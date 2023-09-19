#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from supaword.secure_env import POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_USER, POSTGRES_DB
from tools.utils import read_table_names
from tools.export_db import PostgresDbExport
from tools.import_db import PostgresDbImport
from tools.cleanup_db import PostgresDbCleanup
from supaword.log_helper import logger


def export_data(table_names_file=None, rewrite=True):
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
    table_names = read_table_names(table_names_file)
    logger.info(f"Exporting data from tables: {table_names}")
    db_export.export_to_json(table_names=table_names, rewrite=rewrite)


def import_data(table_names_file=None):
    """
    Import data from JSON files to Postgres database
    """
    db_import = PostgresDbImport(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_ADDRESS,
        port=POSTGRES_PORT
    )
    data_dir = os.path.abspath("tools/import")
    logger.info(f"Importing data from {data_dir}")
    contain_files = [
        f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and f.endswith(".json")
    ]
    if len(contain_files) == 0:
        logger.warning(f"No JSON files found in {data_dir}")
        return

    logger.info(f"Found files: {contain_files}")
    table_names = read_table_names(table_names_file)
    logger.info(f"Importing data from tables: {table_names}")
    db_import.import_tables(table_names=table_names)


def drop_data(table_names_file=None):
    """
    Drop data from Postgres database
    """
    db_cleanup = PostgresDbCleanup(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_ADDRESS,
        port=POSTGRES_PORT
    )
    table_names = read_table_names(table_names_file)
    logger.info(f"Dropping data from tables: {table_names}")
    db_cleanup.drop_tables(table_names=table_names)


def truncate_data(table_names_file=None):
    """
    Truncate data from Postgres database
    """
    db_cleanup = PostgresDbCleanup(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_ADDRESS,
        port=POSTGRES_PORT
    )
    table_names = read_table_names(table_names_file)
    logger.info(f"Truncating data from tables: {table_names}")
    db_cleanup.truncate_tables(table_names=table_names)


def main():
    """
    Run administrative tasks
    """
    command_handlers = {
        "export_data": {
            "handle": export_data,
            "params": ["table_names_file", "restore"]
        },
        "import_data": {
            "handle": import_data,
            "params": ["table_names_file"]
        },
        "drop_data": {
            "handle": drop_data,
            "params": ["table_names_file"]
        },
        "truncate_data": {
            "handle": truncate_data,
            "params": ["table_names_file"]
        }
    }
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supaword.settings')
    command = sys.argv[1] if len(sys.argv) > 1 else None

    def str_to_bool(s):
        return s.lower() in ("true", "yes", "1")

    if command in command_handlers:
        params_num = len(sys.argv) - 2
        expected_params_num = len(command_handlers[command]["params"])
        if params_num == expected_params_num:
            logger.info(f"Executing command '{command}'")
            params_pack = {command_handlers[command]["params"][i]: sys.argv[i + 2] for i in range(params_num)}
            # Check for boolean flags and convert "true" or "false" to boolean values
            for arg_index in range(2, len(sys.argv)):
                if sys.argv[arg_index] in ["true", "false"]:
                    params_pack[command_handlers[command]["params"][arg_index - 2]] = str_to_bool(sys.argv[arg_index])
            logger.info(f"Parameters: {params_pack}")
            command_handlers[command]["handle"](**params_pack)
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
