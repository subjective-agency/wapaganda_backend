import os
import sys
import argparse
import logging
import unicodedata

import supabase.client
from django.core.management.base import BaseCommand
from supaword.log_helper import logger
from supaword.secure_env import SUPABASE_KEY, SUPABASE_URL


def asciify(input_str):
    normalized_string = unicodedata.normalize('NFKD', input_str)
    return ''.join(c for c in normalized_string if ord(c) < 128)


class Command(BaseCommand):
    help = 'Upload files and directories to Supabase Storage'

    def add_arguments(self, parser):
        parser.add_argument('--target-dir', help='Directory to upload files from', default='', required=False)
        parser.add_argument('--target-file', help='File to upload', default='', required=False)
        parser.add_argument('--target-path', help='Relative path to the file in the bucket', default='', required=False)
        parser.add_argument('--bucket-name', help='Name of the bucket to upload to', default='photos', required=False)
        parser.add_argument('--content-type', help='Content type of the file', default='image/jpeg', required=False)

    def handle(self, *args, **options):
        logger.info(
            f'TargetFile="{options["target_file"]}"; TargetDir="{options["target_dir"]}"; '
            f'Bucket={options["bucket_name"]}'
        )
        target_file = options["target_file"]
        target_dir = options["target_dir"]
        target_path = options["target_path"]
        bucket_name = options["bucket_name"]
        content_type = options["content_type"]

        if options["bucket_name"] and options["target_path"] and options["content_type"]:
            if target_file:
                logger.info(
                    f'Uploading file {options["target_file"]} to {options["bucket_name"]}/{options["target_path"]}'
                )
                self.upload_file(local_path=target_file,
                                 bucket_name=bucket_name,
                                 storage_path=target_path,
                                 content_type=content_type)
            elif target_dir:
                logger.info(
                    f'Uploading files from directory {options["target_dir"]} to '
                    f'{options["bucket_name"]}/{options["target_path"]}'
                )
                self.upload_dir(target_dir=target_dir,
                                bucket_name=bucket_name,
                                storage_path=target_path,
                                content_type=content_type)

    @staticmethod
    def upload_file(local_path, bucket_name, storage_path, content_type):
        """
        Upload a file to a Supabase Storage bucket
        :param local_path: path to the file to upload
        :param bucket_name: name of the bucket to upload to
        :param storage_path: relative path to the file in the bucket
        :param content_type: content type of the file, e.g. image/jpeg
        :return:
        """
        local_path = os.path.abspath(local_path)
        if not os.path.isfile(local_path):
            logger.warning(f'File {local_path} does not exist')
            sys.exit(1)

        # get file name from local_path and filter out non-ascii characters
        file_name = asciify(os.path.basename(local_path))
        logger.info(f'Uploading {file_name} to /{bucket_name}/{storage_path}')
        connect = supabase.client.Client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)
        storage = connect.storage()
        storage_bucket = storage.get_bucket(bucket_name)
        try:
            storage_bucket.upload(file=local_path, path=f'{storage_path}/{file_name}', file_options={
                "cacheControl": "3600",
                "content-type": content_type
            })
        except supabase.StorageException as e:
            logger.warning(f'Supabase upload exception: failed to upload {file_name} to {bucket_name}: {e}')
            return False
        except Exception as e:
            logger.error(f'Generic exception: failed to upload {file_name} to {bucket_name}: {e}')
            return False
        return True

    @staticmethod
    def upload_dir(target_dir, bucket_name, storage_path, content_type):
        """
        Upload a directory to a Supabase Storage bucket
        :param target_dir: directory to upload
        :param bucket_name: name of the bucket to upload to
        :param storage_path: relative path to the file in the bucket
        :param content_type: content type of the file, e.g. image/jpeg
        :return:
        """
        if not os.path.isdir(os.path.abspath(target_dir)):
            logger.error(f'Directory {target_dir} does not exist')
            return

        logger.info(f'Processing photos from {target_dir}')
        for file_name in sorted(os.listdir(target_dir)):
            file_name = os.path.join(target_dir, file_name)
            upload_file(local_path=file_name, bucket_name=bucket_name, storage_path=storage_path,
                        content_type=content_type)
