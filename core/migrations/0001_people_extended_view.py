import os
from core.models import TripleLang
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

    operations = [
        TripleLang.Operation(),
        migrations.AddField(model_name='EnumsRucrTaxonomy', name='content', field=TripleLang.Field()),
        migrations.AddField(model_name='EnumsBundleTypes', name='description', field=TripleLang.Field()),
        migrations.AddField(model_name='EnumsISCOTaxonomy', name='term', field=TripleLang.Field()),
        migrations.AddField(model_name='EnumsISCOIndex', name='name', field=TripleLang.Field()),
        migrations.AddField(model_name='EnumsOrgsTaxonomy', name='term', field=TripleLang.Field()),
        migrations.AddField(model_name='EnumsTheoryTypes', name='term', field=TripleLang.Field()),
        migrations.AddField(model_name='MediaSegments', name='name', field=TripleLang.Field()),
        migrations.AddField(model_name='Organizations', name='name', field=TripleLang.Field()),
        migrations.AddField(model_name='Organizations', name='short_name', field=TripleLang.Field()),
        migrations.AddField(model_name='People', name='fullname', field=TripleLang.Field()),
        migrations.AddField(model_name='People', name='lastname', field=TripleLang.Field()),
        migrations.AddField(model_name='People', name='info', field=TripleLang.Field()),
        migrations.AddField(model_name='People', name='known_for', field=TripleLang.Field()),
        migrations.AddField(model_name='PeopleBundles', name='name', field=TripleLang.Field()),
        migrations.AddField(model_name='Printed', name='title', field=TripleLang.Field()),
        migrations.AddField(model_name='Quotes', name='content', field=TripleLang.Field()),
        migrations.AddField(model_name='Theory', name='title', field=TripleLang.Field()),
        migrations.AddField(model_name='Theory', name='excerpt', field=TripleLang.Field()),
        migrations.AddField(model_name='PeopleExtended', name='fullname', field=TripleLang.Field()),
        migrations.AddField(model_name='PeopleExtended', name='lastname', field=TripleLang.Field()),
        migrations.AddField(model_name='PeopleExtended', name='info', field=TripleLang.Field()),
        migrations.AddField(model_name='PeopleExtended', name='known_for', field=TripleLang.Field()),
        create_migration(SQL_DIR)]
