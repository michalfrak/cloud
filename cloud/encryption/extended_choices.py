from enum import Enum


class Choices(Enum):
    """ Possible encryption choices """

    AES_256 = "AES_256"  # Advanced Encryption Standard with 256-bit keys - AWS default
    AES_128 = "AES_128"  # Advanced Encryption Standard with 128-bit keys
