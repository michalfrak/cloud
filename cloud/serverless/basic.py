from abc import ABC, abstractmethod
from typing import Dict


class CloudServerless(ABC):
    """
    Abstract class with definitions of cloud provider serverless functions
    Right now serverless functions and class are based on aws implementations.
    When creating new classes for different providers it needs to be changed to be more
    generic with another providers.
    """

    @abstractmethod
    def invoke(self, **kwargs) -> Dict:
        """ Invoke serverless function and return result dict """
