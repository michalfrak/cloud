import os
from typing import Tuple

from boto3 import Session


class AWSError(Exception):
    pass


def get_boto_session() -> Session:
    return Session(
        aws_access_key_id=os.getenv("DJANGO_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("DJANGO_AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )


def get_bucket_key_from_path(path: str) -> Tuple[str, str]:
    if not path.startswith("s3://"):
        raise AWSError("AWS path must starts with 's3://'")
    try:
        bucket = path.split("s3://")[1].split("/")[0]
        key = path.split("s3://")[1].split("/", 1)[1]
    except IndexError:
        msg = "Incorrect path structure. The proper path examples: s3://bucket/folder/file or s3://bucket/"
        raise AWSError(msg)

    return bucket, key
