# File Name: rz-core-libarary/src/rzcorelibrary/utilities/http/http_request_metadata_provider.py

try:
    from plugins.base import BasePlugin
except ImportError:
    from ....plugins.base import BasePlugin

import ipaddress
import re
import socket
from typing import Union
from django.http import HttpRequest
from rest_framework.request import Request
from .http_request_metadata_model import HttpRequestMetadataModel

class HttpRequestMetadataProvider:

    TRUSTED_HEADERS = (
        "HTTP_CF_CONNECTING_IP",
        "HTTP_TRUE_CLIENT_IP",
        "HTTP_X_REAL_IP",
    )

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # IP - Validation
    # ---------------------------------------------------------

    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        if not ip:
            return False
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    # ---------------------------------------------------------
    # Client IP
    # ---------------------------------------------------------

    @classmethod
    def get_client_ip(cls, request: HttpRequest) -> str:
        for header in cls.TRUSTED_HEADERS:
            ip = request.META.get(header)
            if ip:
                ip = ip.strip()
                if cls._is_valid_ip(ip):
                    return ip

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if x_forwarded_for:
            for ip in x_forwarded_for.split(","):
                ip = ip.strip()
                if cls._is_valid_ip(ip):
                    return ip

        ip = request.META.get("REMOTE_ADDR", "")
        if cls._is_valid_ip(ip):
            return ip

        return ""

    # ---------------------------------------------------------
    # Host IP (Server IP)
    # ---------------------------------------------------------

    @staticmethod
    def get_host_ip(request: HttpRequest) -> str:
        # 1. From WSGI server
        host_ip = request.META.get("SERVER_ADDR", "")
        if host_ip and HttpRequestMetadataProvider._is_valid_ip(host_ip):
            return host_ip

        # 2. Fallback to socket
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            if HttpRequestMetadataProvider._is_valid_ip(ip):
                return ip
        except Exception:
            pass

        return "127.0.0.1"

    # ---------------------------------------------------------
    # User Agent
    # ---------------------------------------------------------

    @staticmethod
    def get_user_agent(request: HttpRequest) -> str:
        return request.headers.get(
            "User-Agent",
            request.META.get("HTTP_USER_AGENT", "")
        )

    # ---------------------------------------------------------
    # Browser
    # ---------------------------------------------------------

    @classmethod
    def get_browser(cls, request: HttpRequest) -> tuple[str, str]:
        ua = cls.get_user_agent(request)
        patterns = [
            (r"Edg/([\d.]+)", "Edge"),
            (r"OPR/([\d.]+)", "Opera"),
            (r"Chrome/([\d.]+)", "Chrome"),
            (r"Firefox/([\d.]+)", "Firefox"),
            (r"Version/([\d.]+).*Safari", "Safari"),
        ]
        for pattern, browser in patterns:
            match = re.search(pattern, ua)
            if match:
                return browser, match.group(1)
        return "Unknown", ""

    # ---------------------------------------------------------
    # Operating System
    # ---------------------------------------------------------

    @classmethod
    def get_os(cls, request: HttpRequest) -> tuple[str, str]:
        ua = cls.get_user_agent(request)
        patterns = [
            (r"Windows NT 10.0", ("Windows", "10/11")),
            (r"Windows NT 6.3", ("Windows", "8.1")),
            (r"Windows NT 6.2", ("Windows", "8")),
            (r"Windows NT 6.1", ("Windows", "7")),
            (r"Android ([\d.]+)", ("Android", None)),
            (r"iPhone OS ([\d_]+)", ("iOS", None)),
            (r"CPU OS ([\d_]+)", ("iOS", None)),
            (r"Mac OS X ([\d_]+)", ("macOS", None)),
            (r"Linux", ("Linux", "")),
        ]
        for pattern, result in patterns:
            match = re.search(pattern, ua)
            if match:
                if result[1] is None:
                    return result[0], match.group(1).replace("_", ".")
                return result
        return "Unknown", ""

    # ---------------------------------------------------------
    # Device Type
    # ---------------------------------------------------------

    @classmethod
    def get_device_type(cls, request: HttpRequest) -> str:
        ua = cls.get_user_agent(request).lower()
        if "bot" in ua:
            return "Bot"
        if "tablet" in ua or "ipad" in ua:
            return "Tablet"
        if "mobile" in ua:
            return "Mobile"
        return "Desktop"

    # ---------------------------------------------------------
    # Host / Method / Referer
    # ---------------------------------------------------------

    @staticmethod
    def get_host(request: HttpRequest) -> str:
        return request.get_host()

    @staticmethod
    def get_method(request: HttpRequest) -> str:
        return request.method or ""

    @staticmethod
    def get_referer(request: HttpRequest) -> str:
        return request.headers.get(
            "Referer",
            request.META.get("HTTP_REFERER", "")
        )

    # ---------------------------------------------------------
    # RequestInfoModel
    # ---------------------------------------------------------

    @classmethod
    def get(cls, request: Union[HttpRequest, Request]) -> HttpRequestMetadataModel:
        browser, browser_version = cls.get_browser(request)
        os_name, os_version = cls.get_os(request)

        return HttpRequestMetadataModel(
            ip_address=cls.get_client_ip(request),
            host_ip=cls.get_host_ip(request),
            user_agent=cls.get_user_agent(request),
            browser=browser,
            browser_version=browser_version,
            os=os_name,
            os_version=os_version,
            device_type=cls.get_device_type(request),
            host=cls.get_host(request),
            method=cls.get_method(request),
            referer=cls.get_referer(request),
        )

class Plugin(BasePlugin):
    name = "http_request_metadata_provider"
    version = "1.0.0"
    description = "HTTP request metadata provider"

    def get_util(self):
        return HttpRequestMetadataProvider