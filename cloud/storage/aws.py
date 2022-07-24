import io
import logging
from typing import BinaryIO, List

from botocore.exceptions import ClientError

from cloud.common.aws import get_boto_session, get_bucket_key_from_path

from .basic import CloudStorage

logger = logging.getLogger(__name__)


class Storage(CloudStorage):
    """ Storage class for aws """

    def __init__(self):
        boto3_session = get_boto_session()
        self.client = boto3_session.client("s3")

    def load_file(self, s3_file_path: str) -> BinaryIO:
        """Load file from S3 bucket

        :param s3_file_path: Path to file on S3 bucket
        Returns: BinaryIO object with file data
        """
        bucket, key = get_bucket_key_from_path(s3_file_path)
        boto3_file_obj = self.client.get_object(
            Bucket=bucket,
            Key=key,
        )["Body"].read()
        file_obj = io.BytesIO(boto3_file_obj)
        return file_obj

    def save_file(self, file_obj: BinaryIO, s3_path: str) -> None:
        """Save file on S3 bucket

        :param file_obj: BinaryIO object with file data
        :param s3_path: srt with S3 path where file should be stored
        """
        bucket, key = get_bucket_key_from_path(s3_path)
        self.client.upload_fileobj(file_obj, bucket, key)

    def list_files(self, path: str) -> List[str]:
        """List files stored on S3 bucket

        :param path: str with S3 path to folder
        Returns: List of files stored under this path
        """

        def update_objs_list() -> None:
            for key_obj in response["Contents"]:
                objs_list.append(key_obj["Key"])

        bucket, key = get_bucket_key_from_path(path)
        response = self.client.list_objects_v2(
            Bucket=bucket,
            Prefix=key,
        )
        objs_list = []
        update_objs_list()

        # Handle pagination. AWS returns up to 1000 keys
        while response["IsTruncated"]:
            response = self.client.list_objects_v2(
                Bucket=bucket,
                Prefix=key,
                ContinuationToken=response["NextContinuationToken"],
            )
            update_objs_list()

        return [obj for obj in objs_list if "/" not in obj]

    def copy_file(self, source_path: str, destination_path: str) -> None:
        """Copy file from one location on S3 bucket to another location on S3

        :param source_path: str with object (file or folder) source path on S3 bucket
        :param destination_path: str with destination path on S3 bucket
        """
        s_bucket, s_key = get_bucket_key_from_path(source_path)
        d_bucket, d_key = get_bucket_key_from_path(destination_path)
        source = {"Bucket": s_bucket, "Key": s_key}
        source_file_name = s_key.split("/")[-1]

        if d_key.endswith("/"):
            d_key = f"{d_key}{source_file_name}"
        if not d_key:
            d_key = source_file_name

        self.client.copy(source, d_bucket, d_key)

    def delete(self, path: str) -> None:
        """Delete object (file or folder) from S3 bucket

        :param path: str with path to S3 object (file or folder)
        """
        bucket, key = get_bucket_key_from_path(path)
        try:
            self.client.delete_object(
                Bucket=bucket,
                Key=key,
            )
        except ClientError as e:
            msg = f"Error deleting the transform file at s3://{bucket}/{key} - {e}"
            logger.error(msg)
            raise e

    def move_file(self, source_path, destination_path) -> None:
        """Move file from one location to another on S3 bucket

        :param source_path: str with file source path on S3 bucket
        :param destination_path: str with destination path on S3 bucket
        """
        self.copy_file(source_path, destination_path)
        self.delete(source_path)

    def create_folder(self, name, path):
        """Create folder on S3 bucket

        :param name: str with name of the folder
        :param path: str with path to folder on S3
        """
        bucket, key = get_bucket_key_from_path(path)
        self.client.put_object(Bucket=bucket, Key=f"{key}{name}/")
