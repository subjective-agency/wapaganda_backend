#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import urllib.request
import zipfile
import io

FRONTEND_VERSION = '0.2.17'


def fetch_static(version):
    """
    Fetch and unpack archive with static files from to static folder, e.g.
    https://wapaganda-frontend.s3.amazonaws.com/builds/wapaganda_frontend-0.2.11.zip
    """

    url = f"https://wapaganda-frontend.s3.amazonaws.com/builds/wapaganda-frontend-{version}.zip"
    print(f"Fetching {url}")
    response = urllib.request.urlopen(url)

    if response.status == 200:
        print(f"Successfully fetched from {url}")
        with zipfile.ZipFile(io.BytesIO(response.read())) as archive:
            archive.extractall("static")
    else:
        print(f"Failed to fetch static files. Status code: {response.status}")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supaword.settings')

    # Check if PROFILE_TYPE is not 'prod' which we do not support yet
    if os.environ.get('PROFILE_TYPE') == 'prod':
        print("Production profile is not supported yet")
        sys.exit(0)

    # This option is our custom option to fetch static files from AWS S3 or Supaword CDN
    if len(sys.argv) > 1 and sys.argv[1] == 'fetchstatic':
        version = sys.argv[2] if len(sys.argv) > 2 else FRONTEND_VERSION
        fetch_static(version)
        sys.exit(0)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
