from abc import ABC
from typing import Dict

from .basic import CloudServerless


class Serverless(CloudServerless, ABC):
    def invoke(self, **kwargs) -> Dict:
        """ Invoke lambda call """
