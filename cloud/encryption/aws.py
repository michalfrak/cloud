import os
from datetime import datetime

from cryptography.fernet import Fernet

from cloud.common.aws import get_boto_session

from .basic import CloudEncryptionKeyManager
from .extended_choices import Choices


class EncryptionKeyManager(CloudEncryptionKeyManager):
    """ Encryption key manager class for aws """

    def __init__(self):
        boto3_session = get_boto_session()
        self.client = boto3_session.client("kms")

    def generate_master_key(self) -> str:
        """Create a KMS Customer Master Key
        The created CMK is a Customer-managed key stored in AWS KMS.

        :return KeyId: AWS globally-unique string ID
        """
        description = f"Common repository encryption master key {datetime.timestamp(datetime.now())}"
        response = self.client.create_key(Description=description)
        return response["KeyMetadata"]["KeyId"]

    def get_master_key_id(self, name: str) -> str:
        """Retrieve an existing KMS CMK based on its description

        :param name: Description of CMK specified when the CMK was created
        :return KeyId: CMK ID
        """
        response = self.client.list_keys()

        done = False
        while not done:
            for cmk in response["Keys"]:
                key_info = self.client.describe_key(KeyId=cmk["KeyArn"])
                if key_info["KeyMetadata"]["Description"] == name:
                    return cmk["KeyId"]
            if not response["Truncated"]:
                done = True
            else:
                response = self.client.list_keys(Marker=response["NextMarker"])

    def generate_data_key(self) -> bytes:
        """Generate AWS data key encrypted by AWS master key to use when encrypting and decrypting data

        :return EncryptedDataKey: Encrypted CiphertextBlob data key as binary string
        """
        cmk_id = os.getenv("AWS_KMS_MASTER_KEY")
        response = self.client.generate_data_key(
            KeyId=cmk_id, KeySpec=Choices.AES_256.value
        )
        return response["CiphertextBlob"]

    def encrypt(self, input_data: bytes, data_key: bytes) -> bytes:
        """Encrypt data

        :param input_data: Data to encrypt
        :param data_key: Data key
        :return Encrypted data
        """
        f = Fernet(data_key)
        return f.encrypt(input_data)

    def decrypt(self, input_data: bytes, data_key: bytes) -> bytes:
        """Decrypt data

        :param input_data: Data to decrypt
        :param data_key: Data key
        :return Decrypted data
        """
        f = Fernet(data_key)
        return f.decrypt(input_data)
