# File Name: rz-core-libarary/src/rzcorelibrary/language/mapping/language_mapping.py

try:
    from plugins.base import BasePlugin
except ImportError:
    try:
        from ....plugins.base import BasePlugin
    except ImportError:
        BasePlugin = object

from abc import ABC, abstractmethod
from typing import Dict
from ..type.language_type import LanguageType

class LanguageMapping(ABC):
    from_language: LanguageType
    to_language: LanguageType

    mapping: Dict[str, str] = {}

class Plugin(BasePlugin):
    name = "language_mapping"
    version = "1.0.0"
    description = "Abstract base class for language mappings"
    def get_util(self):
        return LanguageMapping