#!/usr/bin/env python
"""Django's command-line utility for administrative tasks"""
import os
from django.core.management.base import BaseCommand
from tools.supabase_uploader import SupabaseUploader
from supaword.secure_env import API_KEY, DB_URL
from supaword.log_helper import logger


class Command(BaseCommand):
    help = 'Upload files or directories to Supabase'

    def add_arguments(self, parser):
        parser.add_argument('target_path', help='Local path of the file or directory to upload')
        parser.add_argument('--bucket-name', help='Name of the bucket to upload to', default='photos')
        parser.add_argument('--storage-path', help='Relative path to store the file in the bucket', default='')
        parser.add_argument('--content-type', help='Content type of the file', default='image/jpeg')

    def handle(self, *args, **options):
        # Get the arguments from options
        target_path = options['target_path']
        bucket_name = options['bucket_name']
        storage_path = options['storage_path']
        content_type = options['content_type']

        # Initialize the SupabaseUploader with your settings
        uploader = SupabaseUploader(db_url=DB_URL, api_key=API_KEY)

        # Check if the target path is a file or directory
        if os.path.isfile(target_path):
            uploader.upload_file(local_path=target_path,
                                 bucket_name=bucket_name,
                                 storage_path=storage_path,
                                 content_type=content_type)
            logger.info(f'Uploaded file: {target_path}')
        elif os.path.isdir(target_path):
            uploader.upload_dir(target_dir=target_path,
                                bucket_name=bucket_name,
                                storage_path=storage_path,
                                content_type=content_type)
            logger.info(f'Uploaded files from directory: {target_path}')
        else:
            logger.error(f'Path {target_path} does not exist or is neither a file nor a directory')
