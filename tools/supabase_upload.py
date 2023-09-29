# -*- coding: utf-8 -*-
import os
import sys
import argparse
import logging
import unicodedata
import supabase
from supaword.secure_env import API_KEY, DB_URL
from supaword.log_helper import logger


__doc__ = """Command-line client for uploading photos to Supabase
Photos come in 3 sizes
Large photos size: 1116x1181
Medium photos size: 554x559
Thumbnails size: 204x216

Command example:
python3 supabase_upload.py --target-dir ~/Downloads/faces2
"""
ALL_PEOPLE = {}


class SupabaseUploader:
    def __init__(self, db_url, api_key):
        self.db_url = db_url
        self.api_key = api_key
        self.connect = supabase.Client(db_url, api_key)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def asciify(input_str):
        """
        Normalize the string to decompose combined characters and remove non-ascii characters, e.g. 'é' -> 'e'
        :param input_str: input string with extended characters, e.g. 'é'
        :return: normalized string
        """
        normalized_string = unicodedata.normalize('NFKD', input_str)
        return ''.join(c for c in normalized_string if ord(c) < 128)

    def upload_file(self, local_path, bucket_name, storage_path, content_type):
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
            self.logger.warning(f'File {local_path} does not exist')
            sys.exit(1)

        file_name = self.asciify(os.path.basename(local_path))
        self.logger.info(f'Uploading {file_name} to /{bucket_name}/{storage_path}')
        storage = self.connect.storage()
        storage_bucket = storage.get_bucket(bucket_name)
        try:
            storage_bucket.upload(file=local_path, path=f'{storage_path}/{file_name}', file_options={
                "cacheControl": "3600",
                "content-type": content_type
            })
        except supabase.StorageException as e:
            self.logger.warning(f'Supabase upload exception: failed to upload {file_name} to {bucket_name}: {e}')
        except Exception as e:
            self.logger.error(f'Generic exception: failed to upload {file_name} to {bucket_name}: {e}')

    def upload_dir(self, target_dir, bucket_name, storage_path, content_type):
        """
        Upload a directory to a Supabase Storage bucket
        :param target_dir: directory to upload
        :param bucket_name: name of the bucket to upload to
        :param storage_path: relative path to the file in the bucket
        :param content_type: content type of the file, e.g. image/jpeg
        :return:
        """
    if not os.path.isdir(os.path.abspath(target_dir)):
        self.logger.error(f'Directory {target_dir} does not exist')
        sys.exit(1)

    self.logger.info(f'Processing photos from {target_dir}')
    for file_name in sorted(os.listdir(target_dir)):
        file_name = os.path.join(target_dir, file_name)
        self.upload_file(local_path=file_name, bucket_name=bucket_name, storage_path=storage_path,
                         content_type=content_type)


def main():
    """
    :return: system exit code
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target-dir',
                        help='Directory to upload files from',
                        default='',
                        required=False)
    parser.add_argument('--target-file',
                        help='File to upload',
                        default='',
                        required=False)
    parser.add_argument('--target-path',
                        help='Relative path to the file in the bucket',
                        default='',
                        required=False)
    parser.add_argument('--bucket-name',
                        help='Name of the bucket to upload to',
                        default='photos',
                        required=False)
    parser.add_argument('--content-type',
                        help='Content type of the file',
                        default='image/jpeg',
                        required=False)
    parser.add_argument('--db-url',
                        help='Supabase database URL',
                        required=True)
    parser.add_argument('--api-key',
                        help='Supabase API key',
                        required=True)

    args = parser.parse_args()
    uploader = SupabaseUploader(args.db_url, args.api_key)

    logger.info(f'TargetFile="{args.target_file}"; TargetDir="{args.target_dir}"; Bucket={args.bucket_name}')

    if args.bucket_name and args.target_path and args.content_type:
        if args.target_file:
            uploader.upload_file(local_path=args.target_file, bucket_name=args.bucket_name,
                                 storage_path=args.target_path, content_type=args.content_type)
        elif args.target_dir:
            uploader.upload_dir(target_dir=args.target_dir, bucket_name=args.bucket_name,
                                storage_path=args.target_path, content_type=args.content_type)
    return 0


if __name__ == '__main__':
    sys.exit(main())
