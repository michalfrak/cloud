from abc import ABC, abstractmethod


class CloudEncryptionKeyManager(ABC):
    """ Abstract class with definitions of cloud provider encryption key manager """

    @abstractmethod
    def generate_master_key(self) -> bytes:
        """ Generate encryption master key """
        pass

    @abstractmethod
    def get_master_key_id(self, name: str) -> str:
        """ Return already created master key """
        pass

    @abstractmethod
    def generate_data_key(self) -> bytes:
        """ Generate encryption data key """
        pass

    @abstractmethod
    def encrypt(self, input_data: bytes, data_key: bytes) -> bytes:
        """ Encrypt data """
        pass

    @abstractmethod
    def decrypt(self, input_data: bytes, data_key: bytes) -> bytes:
        """ Decrypt data """
        pass
