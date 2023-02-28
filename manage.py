#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import urllib.request
from urllib.error import HTTPError
import zipfile
import io

FRONTEND_VERSION = '0.2.17'
URLS = [
    f'https://svfizyfozagyqkkjzqdc.supabase.co/storage/v1/object/public/packages/frontend/',
    f'https://wapaganda-frontend.s3.amazonaws.com/builds/'
]


def fetch_static(urls, version):
    """
    Fetch static files from the given urls, unpack to static if successful
    """
    for url in urls:
        archive_name = f'wapaganda-frontend-{version}.zip'
        archive_url = f'{url}{archive_name}'

        try:
            print(f"Try fetching {archive_url}")
            response = urllib.request.urlopen(archive_url)

            if response.status == 200:
                print(f"Extracting zip from {archive_url}")
                with zipfile.ZipFile(io.BytesIO(response.read())) as archive:
                    archive.extractall("static")
                extracted_files = os.listdir("static/build")
                extracted_to = os.path.abspath("static/build")
                print(f"Successfully extracted to {extracted_to} following static files: {extracted_files}")
                return
            else:
                print(f"Failed to fetch static files, trying the next. Status code: {response.status}")
                continue

        except HTTPError as e:
            print(f"Failed to fetch static files, trying the next. Return code {e.code}")
            continue


def main():
    """
    Run administrative tasks
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supaword.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if len(sys.argv) > 1 and sys.argv[1] == 'fetchstatic':
        version = sys.argv[2] if len(sys.argv) > 2 else FRONTEND_VERSION
        fetch_static(URLS, version)
        sys.exit(0)

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
