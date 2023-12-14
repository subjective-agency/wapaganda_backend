import os

from django.db import migrations

SQL_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sql")


def create_migration(directory):
    operations = []
    # Iterate over SQL files in the specified directory
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.sql'):
            with open(os.path.join(directory, filename), 'r') as file:
                sql_content = file.read()
                operations.append(migrations.RunSQL(sql_content))

    return operations


class Migration(migrations.Migration):
    """
    View comprises data on the relevant patients, both from the people table,
    and elsewhere in the DB
    """

    dependencies = []

    operations = create_migration(SQL_DIR)
