#!/usr/bin/env python
"""Django's command-line utility for administrative tasks"""
import os
from django.core.management.base import BaseCommand, CommandError
from supaword.secure_env import POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_USER, POSTGRES_DB
from tools.utils import read_table_names
from tools.export_db import PostgresDbExport
from supaword.log_helper import logger


class Command(BaseCommand):
    help = 'Validate Theory table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_names = ""
        self.bool_rewrite_tables = False
        self.bool_continue_export = False

    def add_arguments(self, parser):
        parser.add_argument('table_name', type=str, help='File containing table names')

    def validate_theory(self):
        """
        Export data from Postgres database to JSON files
        """
        theory_validator = ValidateTheoryTable(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_ADDRESS,
            port=POSTGRES_PORT
        )
        theory_validator.connect_to_database()
        theory_validator.validate_metadata_dates()

    def handle(self, *args, **options):
        self.table_name = options['table_names_file']
        logger.info(f"Table name file: {self.table_name}")
        self.validate_theory()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully validated table: {self.table_name}'
        ))

    