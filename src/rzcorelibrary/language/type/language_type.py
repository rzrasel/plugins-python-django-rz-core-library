# File Name: rz-core-libarary/src/rzcorelibrary/language/type/language_type.py

try:
    from plugins.base import BasePlugin
except ImportError:
    try:
        from ....plugins.base import BasePlugin
    except ImportError:
        BasePlugin = object

from enum import Enum
from typing import cast, Optional

class LanguageType(Enum):

    BANGLA = "bangla"
    # BN = "bangla"
    HINDI = "hindi"
    ENGLISH = "english"
    # EN = "english"

    def __init__(self, slug: str):
        self.slug = slug

    @classmethod
    def from_value(cls, value: Optional[str]) -> Optional["LanguageType"]:
        if not value:
            return None
        value = value.strip().lower()
        for member in cls.__members__.values():
            if member.value == value:
                return member
        return None

class Plugin(BasePlugin):
    name = "language_type"
    version = "1.0.0"
    def get_util(self):
        return LanguageType