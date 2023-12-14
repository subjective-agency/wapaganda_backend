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
    
    dependencies = [
        'organization_type',
        'organizations',
        'media_segments',
        'youtube_channels',
        'rutube_channels',
        'media_roles',
        'ntv_episodes',
        'komso_episodes',
        'smotrim_episodes',
        'youtube_vids',
        'rutube_vids',
        'people',
        'websites',
        'theory',
        'quotes',
        'photos',
        'people_bundles',
        'days_of_war',
        'telegram_channels',
        'telegram_authors',
        'text_media',
        'printed',
        'printed_to_people_mapping',
        'youtube_authors',
        'people_to_msegments_mapping',
        'people_on_youtube',
        'people_on_smotrim',
        'people_on_photos',
        'people_in_orgs',
        'people_in_bundles',
        'people_3rdprt_details_raw',
        'msegments_to_ychannels_mapping',
        'msegments_to_rchannels_mapping',
    ]

    operations = create_migration(SQL_DIR)
