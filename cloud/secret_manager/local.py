from .basic import CloudSecretManager


class SecretManager(CloudSecretManager):
    """ Secret manager class for local environment """

    def get_secret_string(self, secret_name: str) -> str:
        """ Return secret string """
        raise NotImplementedError
