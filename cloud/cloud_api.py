from typing import Optional

from cloud.const import CloudProviderType
from cloud.logger.basic import CloudLogger
from cloud.secret_manager.basic import CloudSecretManager
from cloud.serverless.basic import CloudServerless
from cloud.storage.basic import CloudStorage


class CloudApi:
    """ Class that defines functionality provided by cloud provider """

    def __init__(self, cloud_provider: CloudProviderType) -> None:
        """ Initialize cloud api according to provider type set for environment """

        self.cloud_provider: CloudProviderType = cloud_provider
        self.logger: Optional[CloudLogger] = None
        self.secret_manager: Optional[CloudSecretManager] = None
        self.storage: Optional[CloudStorage] = None
        self.serverless: Optional[CloudServerless] = None
        self._init_cloud_components()

    def _init_cloud_components(self) -> None:
        """ Initialize components for cloud provider """

        if self.cloud_provider == CloudProviderType.AWS:
            from cloud.logger.aws import Logger
            from cloud.secret_manager.aws import SecretManager
            from cloud.storage.aws import Storage
            from cloud.encryption.aws import EncryptionKeyManager
            from cloud.serverless.aws import Serverless

        else:
            from cloud.logger.local import Logger
            from cloud.secret_manager.local import SecretManager
            from cloud.storage.local import Storage
            from cloud.encryption.local import EncryptionKeyManager
            from cloud.serverless.local import Serverless

        self.logger = Logger()
        self.secret_manager = SecretManager()
        self.storage = Storage()
        self.encryption = EncryptionKeyManager()
        self.serverless = Serverless()
