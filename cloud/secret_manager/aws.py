import json
import logging
import os

from boto3.session import Session
from botocore.exceptions import ClientError

from .basic import CloudSecretManager

logger = logging.getLogger(__name__)


class SecretManager(CloudSecretManager):
    """ Secret manager class for aws """

    def __init__(self) -> None:
        """ Initialize secret manager with client session for aws """

        self.client = Session().client(
            service_name="secretsmanager",
            region_name=os.getenv("AWS_REGION"),
        )

    def get_secret_string(self, secret_name: str) -> str:
        """ Return secret string """

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                logger.error("The requested secret " + secret_name + " was not found")
            elif e.response["Error"]["Code"] == "InvalidRequestException":
                logger.error("The request was invalid due to:", e)
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                logger.error("The request had invalid params:", e)
            else:
                logger.error("Error:", e)
        else:
            secret_string = get_secret_value_response["SecretString"]
            secret_dict = json.loads(secret_string)
            return secret_dict
