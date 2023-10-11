#!/usr/bin/env python
"""Django's command-line utility for administrative tasks"""
import os
import subprocess
import argparse
import shutil
from django.core.management.base import BaseCommand, CommandError
from py7zr import SevenZipFile

from supaword.secure_env import POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_USER, POSTGRES_DB
from tools.utils import read_table_names
from tools.export_db import PostgresDbExport
from supaword.log_helper import logger


def on_rm_error(*args):
    """
    In case the file or directory is read-only and we need to delete it
    this function will help to remove 'read-only' attribute
    :param args: (func, path, exc_info) tuple
    """
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    _, path, _ = args
    logger.warning("OnRmError: {0}".format(path))
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


# noinspection PyMethodMayBeStatic
class Command(BaseCommand):
    help = 'Archive export results with 7z'

    def add_arguments(self, parser):
        parser.add_argument('export_dir', type=str,
                            help='Directory where export results (files and subdirs) are stored')
        parser.add_argument('--min-size', type=str, default='1M', required=False,
                            help='Minimum size of file to be archived separately')
        parser.add_argument('--delete-files', action='store_true', default=False, required=False,
                            help='Boolean indicating whether to delete files after archiving')

    def handle(self, *args, **kwargs):
        export_dir = kwargs['export_dir']
        min_size_str = kwargs['min_size'].upper()
        delete_files = kwargs['delete_files'] == 'true'

        # Parse min_size argument to get an appropriate number value
        min_size = self.parse_size_argument(min_size_str)

        # Create a list for files and subfolders that will be archived
        archive_items = []
        remaining_files = []
        os.chdir(os.path.abspath(export_dir))

        for item in os.listdir(os.getcwd()):
            item_path = item
            logger.info(f"Item path: {item_path}")

            if os.path.isdir(item_path):
                archive_items.append(item_path)

            if os.path.isfile(item_path) and item_path.endswith('.json'):
                file_size = os.path.getsize(item_path)

                if file_size >= min_size:
                    archive_items.append(item_path)
                else:
                    remaining_files.append(item_path)

        logger.info(f"Archive items: {archive_items}")
        logger.info(f"Remaining files: {remaining_files}")

        # Archive files and subfolders separately
        for archive_item in archive_items:
            self.archive_file(archive_item)

        # Archive remaining files together
        if len(remaining_files) > 0:
            self.archive_remain(export_dir, remaining_files)

        if delete_files:
            self.cleanup([*archive_items, *remaining_files])

    def parse_size_argument(self, size_str):
        """
        Parse size argument like "1024", "100KB", or "1MB" to get an appropriate number value
        :return: Size in bytes
        """
        multipliers = {'K': 1024, 'M': 1024 ** 2, 'G': 1024 ** 3}
        size_str = size_str.strip()
        size = int(size_str[:-1]) * multipliers.get(size_str[-1], 1)
        return size

    def archive_file(self, file_path):
        """
        Archive a single item using py7zr
        """
        archive_path = f'{file_path}.7z'

        with SevenZipFile(archive_path, 'w') as archive:
            archive.writeall(file_path)

    def archive_remain(self, export_dir, files):
        """
        Archive files together using py7zr
        """
        export_name = os.path.basename(export_dir)
        logger.info(f"Export the rest to public.{export_name}")
        archive_name = f'public.{export_name}.7z'

        with SevenZipFile(archive_name, 'w') as archive:
            for file_path in files:
                archive.writeall(file_path)

    def cleanup(self, items):
        """
        Delete files and subfolders
        """
        for item in items:
            if os.path.isfile(item):
                os.remove(item)
            elif os.path.isdir(item):
                shutil.rmtree(item, onerror=on_rm_error)
