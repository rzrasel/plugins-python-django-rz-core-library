# File Name: rz-core-libarary/src/rzcorelibrary/generator/general/random_id_generator.py

try:
    from plugins.base import BasePlugin
except ImportError:
    from ....plugins.base import BasePlugin

import random
import string
import secrets

class RandomIdGenerator:

    def __new__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__name__} cannot be instantiated."
        )

    @staticmethod
    def get_random_string(length: int = 10) -> str:
        """AlphaNumeric"""
        if length <= 0:
            return ""

        characters = string.ascii_letters + string.digits

        return "".join(
            random.choices(characters, k=length)
        )

    @staticmethod
    def get_secure_random_string(length: int = 10) -> str:
        """Crypto secure - use this for tokens"""
        if length <= 0:
            return ""

        characters = string.ascii_letters + string.digits

        return "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

    @staticmethod
    def get_numeric_string(length: int = 6) -> str:
        if length <= 0:
            return ""

        return "".join(
            random.choices(
                string.digits,
                k=length,
            )
        )

    @staticmethod
    def get_alpha_string(length: int = 10) -> str:
        if length <= 0:
            return ""

        return "".join(
            random.choices(
                string.ascii_letters,
                k=length,
            )
        )

class Plugin(BasePlugin):
    name = "random_id_generator"
    version = "1.0.0"
    description = "Generate random IDs and strings"
    def get_util(self):
        return RandomIdGenerator