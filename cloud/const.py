from enum import Enum


class CloudProviderType(Enum):
    """ Possible cloud providers used in application """

    AWS = "Amazon Web Services"
    AZURE = "Microsoft Azure"
    GOOGLE_CLOUD = "Google Cloud"
    LOCAL = "Local environment"
