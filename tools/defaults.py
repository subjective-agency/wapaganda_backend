TABLE_NAMES = [
    "days_of_war",
    "komso_episodes",
    "media_coverage_type",
    "media_roles",
    "media_segments",
    "msegments_to_rchannels_mapping",
    "msegments_to_ychannels_mapping",
    "ntv_episodes",
    "organization_type",
    "organizations",
    "people",
    "people_3rdprt_details_raw",
    "people_bundles",
    "people_extended",
    "people_in_bundles",
    "people_in_orgs",
    "people_in_ur",
    "people_on_photos",
    "people_on_smotrim",
    "people_on_youtube",
    "people_to_msegments_mapping",
    "photos",
    "printed",
    "printed_to_people_mapping",
    "quotes",
    "rutube_channels",
    "rutube_vids",
    "smotrim_episodes",
    "telegram_authors",
    "telegram_channels",
    "theory",
    "websites",
    "youtube_authors",
    "youtube_channels",
    "youtube_vids"
]


def read_table_names(table_names_file):
    """
    Read table names from file
    """
    table_names = []
    if table_names_file is not None:
        with open(table_names_file, "r") as file:
            [table_names.append(line.strip()) for line in file.readlines() if line.strip() in TABLE_NAMES]
    return table_names
