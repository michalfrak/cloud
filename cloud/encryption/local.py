from .basic import CloudEncryptionKeyManager


class EncryptionKeyManager(CloudEncryptionKeyManager):
    """ Encryption key manager class for local environment """

    def generate_master_key(self) -> bytes:
        """ Generate encryption master key """
        pass

    def get_master_key_id(self, name: str) -> str:
        """ Return already created master key """
        pass

    def generate_data_key(self) -> bytes:
        """ Generate encryption data key """
        pass

    def encrypt(self, input_data: bytes, data_key: bytes) -> bytes:
        """ Encrypt data """
        pass

    def decrypt(self, input_data: bytes, data_key: bytes) -> bytes:
        """ Decrypt data """
        pass
