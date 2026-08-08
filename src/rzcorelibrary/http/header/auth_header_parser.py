# File Name: rz-core-libarary/src/rzcorelibrary/http/header/auth_header_parser.py

try:
    from plugins.base import BasePlugin
except ImportError:
    try:
        from ....plugins.base import BasePlugin
    except ImportError:
        BasePlugin = object

from django.http import HttpRequest
from rest_framework.request import Request
from typing import Union
from typing import Optional

class AuthHeaderParser:

    def __init__(self):
        raise TypeError(
            f"{self.__class__.__name__} cannot be instantiated."
        )

    @staticmethod
    def get_bearer_token(
            request: Union[HttpRequest, Request],
            header_name: str = "Authorization",
            prefix: str = "Bearer",
    ) -> Optional[str]:
        """
        Extracts the Bearer token from request headers.

        Args:
            request: Django HttpRequest or DRF Request object.
            header_name (str): Header name, default "Authorization".
            prefix (str): Token prefix, default "Bearer".

        Returns:
            str | None: Returns the token string if present, else None.
        """
        header_name = header_name.strip()
        prefix = prefix.strip()

        # ─────────────── GET HEADER FROM DRF REQUEST ───────────────
        # Try DRF request.headers first
        auth_header = request.headers.get(header_name)

        # ───────────── FALLBACK TO DJANGO META ─────────────
        # Fallback to Django HttpRequest.META
        if not auth_header:
            meta_key = (
                f"HTTP_{header_name.upper().replace('-', '_')}"
            )
            auth_header = request.META.get(meta_key)

        # ─────────────────── HEADER NOT FOUND ───────────────────

        if not auth_header:
            return None

        auth_header = auth_header.strip()

        # ─────────────── VALIDATE AUTHENTICATION PREFIX ───────────────

        bearer_prefix = f"{prefix} "

        if not auth_header.startswith(bearer_prefix):
            return None

        # ───────────────────── RETURN TOKEN ─────────────────────

        return auth_header[len(bearer_prefix):].strip()

class Plugin(BasePlugin):
    name = "auth_header_parser"
    version = "1.0.0"
    description = "Parse Authorization headers for Bearer tokens"
    def get_util(self):
        return AuthHeaderParser