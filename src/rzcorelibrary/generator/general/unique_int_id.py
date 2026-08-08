# File Name: rz-core-libarary/src/rzcorelibrary/generator/general/unique_int_id.py

try:
    from plugins.base import BasePlugin
except ImportError:
    from ....plugins.base import BasePlugin

import time
import random
from typing import Optional
from .random_id_generator import RandomIdGenerator

class UniqueIntId:

    def __init__(self):
        raise TypeError(
            f"{cls.__name__} cannot be instantiated."
        )

    @staticmethod
    def get_microtime() -> int:
        return round(time.time() * 1000)

    @staticmethod
    def get_random_digit(
            length: int,
            is_start_with_zero: bool = True,
    ) -> str:
        length = int(length)

        if length <= 0:
            return ""

        first_digit = (
            random.randint(0, 9)
            if is_start_with_zero
            else random.randint(1, 9)
        )

        output = str(first_digit)

        for _ in range(length - 1):
            output += str(random.randint(0, 9))

        return output

    @staticmethod
    def get_bigint_id(
            length: int = 4,
            is_start_with_zero: bool = True,
    ) -> int:
        microtime = UniqueIntId.get_microtime()

        random_digit = UniqueIntId.get_random_digit(
            length=length,
            is_start_with_zero=is_start_with_zero,
        )

        return int(
            f"{microtime}{random_digit}"
        )

    @staticmethod
    def get_sys_bigint_user_id(
            user_string: Optional[str] = None,
            length: int = 20,
    ) -> int:
        if not user_string:
            user_string = RandomIdGenerator.get_random_string(50)

        system_user_string = (
                user_string
                + user_string.lower()
                + user_string.upper()
        )

        system_user_id = sum(
            ord(character)
            for character in system_user_string
        )

        system_user_id = int(
            f"{system_user_id}"
            f"{system_user_id * 2}"
            f"{system_user_id * 3}"
        )

        sliced_id = str(system_user_id)[:int(length)]

        return int(sliced_id)

class Plugin(BasePlugin):
    name = "unique_int_id"
    version = "1.0.0"
    description = "Generate unique integer IDs based on microtime and random digits"
    def get_util(self):
        return UniqueIntId