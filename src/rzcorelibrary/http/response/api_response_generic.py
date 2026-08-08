# File Name: rz-core-libarary/src/rzcorelibrary/http/response/api_response_generic.py

try:
    from plugins.base import BasePlugin
except ImportError:
    try:
        from....plugins.base import BasePlugin
    except ImportError:
        BasePlugin = object

from typing import Generic, Optional, TypeVar, Any
T = TypeVar("T")

class ApiResponseGeneric(Generic[T]):

    def __init__(
        self,
        response: bool,
        message: Optional[str],
        data: Optional[T] = None,
        need_user_login: bool = False,
        errors: Optional[T] = None,
        status: int = 200,
        log: Optional[T] = None
    ):
        self.response = response
        self.message = message
        self.data = data
        self.need_user_login = need_user_login
        self.errors = errors
        self.status = status
        self.log = log

class Plugin(BasePlugin):
    name = "api_response_generic"
    version = "1.0.0"
    description = "Generic API response wrapper"
    def get_util(self):
        return ApiResponseGeneric