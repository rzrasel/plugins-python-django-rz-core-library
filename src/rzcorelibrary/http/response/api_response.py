# File Name: rz-core-libarary/src/rzcorelibrary/http/response/api_response.py

try:
    from plugins.base import BasePlugin
except ImportError:
    try:
        from ....plugins.base import BasePlugin
    except ImportError:
        BasePlugin = object

from rest_framework.response import Response
from typing import Generic, Optional, TypeVar, Any, Dict
T = TypeVar("T")

class ApiResponse:

    def __init__(self):
        raise TypeError(
            f"{self.__class__.__name__} cannot be instantiated."
        )

    """
    Standard API response helper for Django REST Framework.
    """

    @staticmethod
    def success(
            response: bool = True,
            message: Optional[str] = "Success",
            data: Optional[T] = None,
            need_user_login: bool = False,
            errors: Optional[T] = None,
            status: int = 200,
            log: Optional[T] = None
    ):
        return Response(
            {
                "response": response,
                "message": message,
                "data": data,
                "need_user_login": need_user_login,
                "errors": errors,
                "status": status,
                "log": log,
            },
            status=status,
        )

    @staticmethod
    def error(
            response: bool = False,
            message: Optional[str] = "Error",
            data: Optional[T] = None,
            need_user_login: bool = False,
            errors: Optional[T] = None,
            status: int = 400,
            log: Optional[T] = None
    ):
        return Response(
            {
                "response": response,
                "message": message,
                "data": data,
                "need_user_login": need_user_login,
                "errors": errors,
                "status": status,
                "log": log,
            },
            status=status,
        )

class Plugin(BasePlugin):
    name = "api_response"
    version = "1.0.0"
    description = "Standard API response helper for DRF"
    def get_util(self):
        return ApiResponse