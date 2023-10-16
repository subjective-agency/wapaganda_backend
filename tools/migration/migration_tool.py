import subprocess
import json


class SnapletWrapper:
    def __init__(self, source_credentials, target_credentials, table_list):
        self.source_credentials = source_credentials
        self.target_credentials = target_credentials
        self.table_list = table_list

    def capture(self):
        creds = self.source_credentials
        source_db_url = (f"postgresql://{creds['POSTGRES_USER']}:{creds['POSTGRES_PASSWORD']}@"
                         f"{creds['POSTGRES_ADDRESS']}:{creds['POSTGRES_PORT']}/{creds['POSTGRES_DB']}")
        print(f"Capturing snapshot from {source_db_url}")
        cmd_export_and_capture = (f'export SNAPLET_SOURCE_DATABASE_URL="{source_db_url}" && snaplet snapshot capture '
                                  f'--transform-mode unsafe')

        subprocess.run(cmd_export_and_capture, shell=True, check=True)

    def restore(self):
        creds = self.target_credentials
        target_db_url = (f"postgresql://{creds['POSTGRES_USER']}:{creds['POSTGRES_PASSWORD']}@"
                         f"{creds['POSTGRES_ADDRESS']}:{creds['POSTGRES_PORT']}/{creds['POSTGRES_DB']}")
        print(f"Restoring snapshot to {target_db_url}")
        cmd_export_target = f'export SNAPLET_DATABASE_URL="{target_db_url}"'
        cmd_restore = f'snaplet snapshot restore --tables {" ".join(self.table_list)}'

        subprocess.run(cmd_export_target, shell=True, check=True)
        subprocess.run(cmd_restore, shell=True, check=True)


def main():
    parser = argparse.ArgumentParser(description="Snaplet Capture and Restore")
    parser.add_argument("--capture", action="store_true", help="Capture a snapshot")
    parser.add_argument("--restore", action="store_true", help="Restore a snapshot")
    args = parser.parse_args()

    # Load credentials from JSON files
    with open('/Users/atatat/.supaword/credentials_prod.json', 'r') as source_file:
        source_credentials = json.load(source_file)

    with open('/Users/atatat/.supaword/credentials_srv.json', 'r') as target_file:
        target_credentials = json.load(target_file)

    table_list = [
        "days_of_war",
        "dentv_episodes",
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
        "text_media",
        "theory",
        "websites",
        "youtube_authors",
        "youtube_channels",
        "youtube_vids"
    ]

    wrapper = SnapletWrapper(
        source_credentials=source_credentials,
        target_credentials=target_credentials,
        table_list=table_list
    )

    if args.capture:
        wrapper.capture()

    if args.restore:
        wrapper.restore()

    if not args.capture and not args.restore:
        wrapper.capture()
        wrapper.restore()


if __name__ == "__main__":
    main()
