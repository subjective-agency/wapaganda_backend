# -*- coding: utf-8 -*-
import os
import json
import pathlib

HOME_DIR = os.path.join(pathlib.Path.home())
CREDENTIALS_FILE = os.path.join(HOME_DIR, '.supaword', 'credentials.json')

__doc__ = """Constants for accessing Supabase database"""


def environment_value(environment_name):
    """
    :param environment_name: Name of the environment variable
    :return: Value of the environment variable or the empty string if not exists
    """
    return os.environ.get(environment_name, '')


# Always keep API_KEY in a safe place, and never commit it to the repository as plain text
def from_credentials_file():
    """
    Check if credentials file exists and return its content
    Always keep API_KEY in a safe place, and never commit it to the repository as plain text!
    :return: Dict from the JSON credentials file or the empty dict if not exists
    """
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as credentials_file:
            return json.load(credentials_file)
    return {}


CREDENTIALS = from_credentials_file()

# General
DB_CONNECTION_STRING = CREDENTIALS.get('CONNECTION_STRING', '') or environment_value('CONNECTION_STRING')

# Postgres
POSTGRES_PASSWORD = CREDENTIALS.get('POSTGRES_PASSWORD', '') or environment_value('POSTGRES_PASSWORD')
POSTGRES_ADDRESS = CREDENTIALS.get('POSTGRES_ADDRESS', '') or environment_value('POSTGRES_ADDRESS')
POSTGRES_USER = CREDENTIALS.get('POSTGRES_USER', '') or environment_value('POSTGRES_USER')
POSTGRES_PORT = int(CREDENTIALS.get('POSTGRES_PORT', 5432)) or int(environment_value('POSTGRES_PORT'))
POSTGRES_DB = CREDENTIALS.get('POSTGRES_DB', '') or environment_value('POSTGRES_DB')

# Snaplet
SNAPLET_SOURCE_DATABASE_URL = DB_CONNECTION_STRING
SNAPLET_DATABASE_URL = DB_CONNECTION_STRING

# Django
DJANGO_KEY = CREDENTIALS.get('DJANGO_KEY', '') or environment_value('DJANGO_KEY')

# Debug
SERVER_DEBUG = CREDENTIALS.get('DEBUG', '0') or environment_value('DEBUG')
SERVER_DEBUG = SERVER_DEBUG.strip()
assert SERVER_DEBUG in (0, 1, "0", "1"), f"DEBUG must be 1 or 0, instead of '{SERVER_DEBUG}, type {type(SERVER_DEBUG)}'"
SERVER_DEBUG = int(SERVER_DEBUG)

assert len(DB_CONNECTION_STRING) > 0, "Connection string is empty"
assert len(POSTGRES_USER) > 0, "Database username is empty"
assert len(POSTGRES_DB) > 0, "Database name is empty"
assert len(POSTGRES_PASSWORD) > 0, "Database password is empty"
assert len(POSTGRES_ADDRESS) > 0, "Postgres address is empty"

assert len(DJANGO_KEY) > 0, "Django key is empty"

assert (DB_CONNECTION_STRING.startswith("postgresql://") or DB_CONNECTION_STRING.startswith("postgres://")), \
    f"Connection string must start with postgresql://, '{DB_CONNECTION_STRING}' instead"
