#!/usr/bin/env python
"""Django's command-line utility for administrative tasks"""
import os
from django.core.management.base import BaseCommand, CommandError
from supaword.secure_env import POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_USER, POSTGRES_DB
from tools.utils import read_table_names
from tools.export_db import PostgresDbExport
from supaword.log_helper import logger


class Command(BaseCommand):
    help = 'Export data from specified tables'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_names_file = []
        self.bool_rewrite_tables = False
        self.bool_continue_export = False

    def add_arguments(self, parser):
        parser.add_argument('table_names_file', type=str, help='File containing table names')
        parser.add_argument('--rewrite-tables', type=str, choices=['true', 'false'],
                            help='Boolean indicating whether to rewrite tables')
        parser.add_argument('--continue-export', type=str, choices=['true', 'false'],
                            help='Boolean indicating whether to continue paused export')

    def export_data(self):
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
        table_names = read_table_names(self.table_names_file)
        logger.info(f"Exporting data from tables: {table_names}")
        db_export.export_to_json(table_names=table_names,
                                 rewrite=self.bool_rewrite_tables,
                                 restore=self.bool_continue_export)

    def handle(self, *args, **options):
        self.table_names_file = options['table_names_file']
        self.bool_rewrite_tables = options['rewrite_tables'] == 'true'  # Convert to boolean
        self.bool_continue_export = options['continue_export'] == 'true'  # Convert to boolean
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
