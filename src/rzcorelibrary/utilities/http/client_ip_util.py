# File Name: rz-core-libarary/src/rzcorelibrary/utilities/http/client_ip_util.py

try:
    from plugins.base import BasePlugin
except ImportError:
    from ....plugins.base import BasePlugin

import ipaddress
from typing import Optional

class ClientIpUtil:
    TRUSTED_HEADERS = (
        "HTTP_CF_CONNECTING_IP",  # Cloudflare
        "HTTP_TRUE_CLIENT_IP",  # Cloudflare Enterprise / Akamai
        "HTTP_X_REAL_IP",  # Nginx
    )

    def __new__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__name__} cannot be instantiated."
        )

    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        if not ip:
            return False

        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str:

        # 1. Trusted proxy headers.
        for header in ClientIpUtil.TRUSTED_HEADERS:
            ip = request.META.get(header, "")

            if not ip:
                continue

            ip = ip.strip()

            if ClientIpUtil._is_valid_ip(ip):
                return ip

        # 2. X-Forwarded-For.
        #
        # X-Forwarded-For can contain multiple addresses:
        #
        # client, proxy1, proxy2
        #
        # The first address is normally the originating client.
        x_forwarded_for = request.META.get(
            "HTTP_X_FORWARDED_FOR",
            "",
        )

        if x_forwarded_for:
            for ip in x_forwarded_for.split(","):
                ip = ip.strip()

                if ClientIpUtil._is_valid_ip(ip):
                    return ip

        # 3. Direct connection fallback.
        remote_addr = request.META.get(
            "REMOTE_ADDR",
            "",
        )

        remote_addr = remote_addr.strip()

        if ClientIpUtil._is_valid_ip(remote_addr):
            return remote_addr

        return ""

class Plugin(BasePlugin):
    name = "client_ip_util"
    version = "1.0.0"
    description = "Get real client IP from Django request"
    def get_util(self):
        return ClientIpUtil