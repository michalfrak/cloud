from abc import ABC, abstractmethod


class CloudSecretManager(ABC):
    """ Abstract class with definitions of cloud provider secret manager """

    @abstractmethod
    def get_secret_string(self, secret_name: str) -> str:
        """ Return secret string """
