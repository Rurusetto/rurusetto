from storages.backends.s3boto3 import S3Boto3Storage
from decouple import config


class StaticStorage(S3Boto3Storage):
    bucket_name = config('AWS_STORAGE_BUCKET_NAME', default="your-storage-bucket-name")
    location = 'static'


class MediaStorage(S3Boto3Storage):
    bucket_name = config('AWS_STORAGE_BUCKET_NAME', default="your-storage-bucket-name")
    location = 'media'
