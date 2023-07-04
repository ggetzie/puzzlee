from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage


class StaticRootS3Boto3Storage(S3ManifestStaticStorage):
    location = "static"
    # default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
