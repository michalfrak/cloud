import os
from .const import CloudProviderType
from .cloud_api import CloudApi

cloud_provider = getattr(CloudProviderType, os.getenv("CLOUD_PROVIDER", "LOCAL"))
cloud_api = CloudApi(cloud_provider=cloud_provider)
