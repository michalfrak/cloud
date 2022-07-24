from unittest.mock import call, patch

import pytest
from boto3 import Session

from cloud import CloudApi, CloudProviderType
from cloud.common.aws import AWSError, get_bucket_key_from_path


def test_should_properly_get_bucket_and_file_key_from_path():
    path = "s3://test-bucket/test_folder/test_file.txt"

    bucket, key = get_bucket_key_from_path(path)

    assert bucket == "test-bucket"
    assert key == "test_folder/test_file.txt"


def test_should_properly_get_bucket_and_folder_key_from_path():
    path = "s3://test-bucket/test_folder/test_folder2/"

    bucket, key = get_bucket_key_from_path(path)

    assert bucket == "test-bucket"
    assert key == "test_folder/test_folder2/"


def test_should_raise_error_when_improper_path_provided():
    with pytest.raises(AWSError):
        get_bucket_key_from_path("s://test-bucket/")


@patch.object(Session, "client")
def test_should_copy_file_when_destination_file_name_is_provided(mock_client):
    source_path = "s3://test-bucket/test_folder/test_file.txt"
    destination_path = "s3://test-bucket/test_folder/test_folder2/new_file_name.txt"
    cloud_api = CloudApi(CloudProviderType.AWS)
    mock_copy = mock_client.return_value.copy
    expected_call_args_list = [
        call(
            {"Bucket": "test-bucket", "Key": "test_folder/test_file.txt"},
            "test-bucket",
            "test_folder/test_folder2/new_file_name.txt",
        )
    ]

    cloud_api.storage.copy_file(source_path, destination_path)

    assert mock_copy.call_args_list == expected_call_args_list


@patch.object(Session, "client")
def test_should_copy_file_when_destination_file_name_is_not_provided(mock_client):
    source_path = "s3://test-bucket/test_folder/test_file.txt"
    destination_path = "s3://test-bucket/test_folder/test_folder2/"
    cloud_api = CloudApi(CloudProviderType.AWS)
    mock_copy = mock_client.return_value.copy
    expected_call_args_list = [
        call(
            {"Bucket": "test-bucket", "Key": "test_folder/test_file.txt"},
            "test-bucket",
            "test_folder/test_folder2/test_file.txt",
        )
    ]

    cloud_api.storage.copy_file(source_path, destination_path)

    assert mock_copy.call_args_list == expected_call_args_list
