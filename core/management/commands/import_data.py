#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
from django.core.management.base import BaseCommand, CommandError
from wganda.secure_env import POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_USER, POSTGRES_DB
from tools.utils import read_table_names
from tools.import_db import PostgresDbImport
from wganda.log_helper import logger


class Command(BaseCommand):
    help = 'Import data into specified tables'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_names_file = None
        self.import_dir = None

    def import_data(self):
        """
        Import data from JSON files to Postgres database
        """
        db_import = PostgresDbImport(
            import_dir=self.import_dir,
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
        table_names = read_table_names(self.table_names_file)
        logger.info(f"Importing data from tables: {table_names}")
        db_import.import_tables(table_names=table_names)
        
    def add_arguments(self, parser):
        parser.add_argument('--table-names',
                            type=str,
                            help='File containing table names')
        parser.add_argument('--import-dir',
                            type=str,
                            required=False,
                            default='tools/export',
                            help='Directory containing data for import')

    def handle(self, *args, **options):
        self.table_names_file = options['table_names']
        self.import_dir = options['import_dir']

        if not os.path.exists(self.table_names_file):
            raise CommandError(f"The specified file '{self.table_names_file}' does not exist.")

        if not os.path.exists(self.import_dir):
            raise CommandError(f"The specified directory '{self.import_dir}' does not exist.")

        self.import_data()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported data into tables specified in file: {self.table_names_file}, '
            f'from exported data directory: {self.import_dir}'
        ))
