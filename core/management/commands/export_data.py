#!/usr/bin/env python
"""Django's command-line utility for administrative tasks"""
import os
from django.core.management.base import BaseCommand, CommandError
from wganda.secure_env import POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_USER, POSTGRES_DB
from tools.utils import read_table_names
from tools.export_db import PostgresDbExport
from wganda.log_helper import logger


class Command(BaseCommand):
    help = 'Export data from specified tables'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_names_file = []
        self.export_dir = ""
        self.bool_rewrite_tables = False
        self.bool_continue_export = False
        self.skip_export = False

    def add_arguments(self, parser):
        parser.add_argument('table_names_file',
                            type=str,
                            help='File containing table names')
        parser.add_argument('--rewrite-tables',
                            type=str,
                            choices=['true', 'false'],
                            default='false',
                            required=False,
                            help='Boolean indicating whether to rewrite tables')
        parser.add_argument('--continue-export',
                            type=str,
                            choices=['true', 'false'],
                            default='false',
                            required=False,
                            help='Boolean indicating whether to continue paused export')
        parser.add_argument('--skip-export',
                            type=str,
                            choices=['true', 'false'],
                            default='false',
                            required=False,
                            help='Boolean indicating whether to skip export if the table up-to-date')
        parser.add_argument('--export-dir',
                            type=str,
                            required=False,
                            default='tools/export',
                            help='Directory to store exported data')

    def export_data(self):
        """
        Export data from Postgres database to JSON files
        """
        db_export = PostgresDbExport(
            export_dir=self.export_dir,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_ADDRESS,
            port=POSTGRES_PORT
        )
        table_names = read_table_names(self.table_names_file)
        logger.info(f"Exporting data from tables: {table_names}")
        db_export.export_to_json(table_names=table_names,
                                 rewrite=self.bool_rewrite_tables,
                                 restore=self.bool_continue_export)

    def handle(self, *args, **options):
        self.table_names_file = options['table_names_file']
        self.export_dir = options['export_dir']
        # Convert to boolean
        self.bool_rewrite_tables = options['rewrite_tables'] == 'true'
        self.bool_continue_export = options['continue_export'] == 'true'
        self.skip_export = options['skip_export'] == 'true'

        logger.info(f"Table name file: {self.table_names_file}")
        logger.info(f"Rewrite Tables: {self.bool_rewrite_tables}")
        logger.info(f"Resume Export: {self.bool_continue_export}")

        if not os.path.exists(self.table_names_file):
            raise CommandError(f"The specified file '{self.table_names_file}' does not exist")
        self.export_data()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully exported data from file: {self.table_names_file}, '
            f'Rewrite Tables: {self.bool_rewrite_tables}, '
            f'Continue Paused Export: {self.bool_continue_export}'
        ))
