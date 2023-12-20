#!/usr/bin/env python
"""Django's command-line utility for administrative tasks"""
import os
from django.core.management.base import BaseCommand, CommandError
from wganda.secure_env import POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_USER, POSTGRES_DB
from tools.table_validator import TableValidator
from wganda.log_helper import logger


class Command(BaseCommand):
    help = 'Validate Theory table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = ""

    def add_arguments(self, parser):
        parser.add_argument('table_name', type=str, help='Table name to validate')

    def validate_theory(self):
        """
        Export data from Postgres database to JSON files
        """
        validator = TableValidator(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_ADDRESS,
            port=POSTGRES_PORT
        )
        validator.connect_to_database()
        validator.validate_table(self.table_name)
        validator.close_connection()

    def handle(self, *args, **options):
        self.table_name = options['table_name']
        logger.info(f"Table name: {self.table_name}")
        self.validate_theory()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully validated table: {self.table_name}'
        ))
    