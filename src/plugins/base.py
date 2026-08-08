from abc import ABC, abstractmethod
from typing import Any

class BasePlugin(ABC):
    """
    Base class for all rz-core-library plugins
    Every plugin in src/rzcorelibrary/utilities/ and security/ must inherit this
    """
    name: str = ""
    version: str = "1.0.0"
    description: str = ""

    @abstractmethod
    def get_util(self) -> Any:
        """
        Return the utility class
        Example: return StringUtils
        """
        pass

    def get_info(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description
        }