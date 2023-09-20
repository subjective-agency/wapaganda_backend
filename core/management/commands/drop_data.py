#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
from django.core.management.base import BaseCommand, CommandError
from supaword.secure_env import POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_USER, POSTGRES_DB
from tools.utils import read_table_names
from tools.cleanup_db import PostgresDbCleanup
from supaword.log_helper import logger


class Command(BaseCommand):
    help = 'Drop specified database tables'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_names_file = None

    def add_arguments(self, parser):
        parser.add_argument('table_names_file',
                            type=str,
                            help='File containing table names to drop')

    def drop_data(self):
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
        table_names = read_table_names(self.table_names_file)
        logger.info(f"Dropping data from tables: {table_names}")
        db_cleanup.drop_tables(table_names=table_names)

    def handle(self, *args, **options):
        self.table_names_file = options['table_names_file']

        if not os.path.exists(self.table_names_file):
            raise CommandError(f"The specified file '{self.table_names_file}' does not exist.")

        self.drop_data()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully dropped tables specified in file: {self.table_names_file}'
        ))
