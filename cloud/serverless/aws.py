import logging
import os
from typing import Dict

from boto3 import client

from .basic import CloudServerless

logger = logging.getLogger(__name__)


class Serverless(CloudServerless):
    def __init__(self) -> None:
        """ Initialize secret manager with client session for aws """

        self.client = client("lambda", region_name=os.getenv("AWS_REGION"))

    def invoke(self, **kwargs) -> Dict:
        """ Invoke lambda call """

        result = self.client.invoke(**kwargs)
        if "FunctionError" in result:
            logger.error(f"Error in invoking import pipeline done signal: {result}")
        return result
