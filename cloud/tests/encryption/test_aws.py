from unittest.mock import patch

from boto3 import Session

from cloud import CloudApi, CloudProviderType


@patch.object(Session, "client")
def test_should_properly_get_master_key_id_after_it_is_created(mock_session):
    mock_generate_key = mock_session.return_value.create_key
    mock_generate_key.return_value = {"KeyMetadata": {"KeyId": "UniqueAWSId"}}
    expected_output = "UniqueAWSId"
    cloud_api = CloudApi(CloudProviderType.AWS)

    output = cloud_api.encryption.generate_master_key()

    assert output == expected_output


@patch.object(Session, "client")
def test_should_properly_get_master_key_id_from_description(mock_session):
    mock_list_keys = mock_session.return_value.list_keys
    mock_list_keys.return_value = {
        "Keys": [
            {
                "KeyId": "UniqueAWSId01",
                "KeyArn": "arn:aws:kms:identifier01",
            },
        ],
        "Truncated": False,
    }
    mock_describe_key = mock_session.return_value.describe_key
    mock_describe_key.return_value = {
        "KeyMetadata": {
            "KeyId": "UniqueAWSId01",
            "Arn": "arn:aws:kms:identifier01",
            "Description": "Test_key_description",
        },
    }
    cloud_api = CloudApi(CloudProviderType.AWS)
    expected_output = "UniqueAWSId01"

    output = cloud_api.encryption.get_master_key_id("Test_key_description")

    assert output == expected_output


@patch.object(Session, "client")
def test_should_return_encrypted_version_of_data_key(mock_session):
    mock_generate_data_key = mock_session.return_value.generate_data_key
    mock_generate_data_key.return_value = {
        "CiphertextBlob": b"\x01\x02\x03\x00x\xa2RtQW\x85",
        "Plaintext": b"\x81\xb0\x05\xe2\x84",
        "KeyId": "arn:aws:kms:test_key_id",
    }
    cloud_api = CloudApi(CloudProviderType.AWS)
    expected_output = b"\x01\x02\x03\x00x\xa2RtQW\x85"

    output = cloud_api.encryption.generate_data_key()

    assert output == expected_output


@patch.object(Session, "client")
def test_should_properly_encrypt_and_decrypt_data(_):
    data_key = b"vGP6jvBPU9j8qXHCx3CfuwE440AEqB2opm7udPeWP4Q="
    cloud_api = CloudApi(CloudProviderType.AWS)
    initial_test_value = b"initial test value"

    data_encrypted = cloud_api.encryption.encrypt(initial_test_value, data_key)
    data_decrypted = cloud_api.encryption.decrypt(data_encrypted, data_key)

    assert data_decrypted == initial_test_value
