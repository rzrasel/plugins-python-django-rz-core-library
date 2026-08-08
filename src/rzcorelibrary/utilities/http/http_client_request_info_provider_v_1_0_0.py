import ipaddress
import re
from django.http import HttpRequest
from .http_request_metadata_model import HttpRequestMetadataModel

class HttpClientRequestInfoProvider_V_1_0_0:

    TRUSTED_HEADERS = (
        "HTTP_CF_CONNECTING_IP",
        "HTTP_TRUE_CLIENT_IP",
        "HTTP_X_REAL_IP",
    )

    def __init__(self):
        raise TypeError(
            f"{self.__class__.__name__} cannot be instantiated."
        )

    # ---------------------------------------------------------
    # IP
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

    @classmethod
    def get_client_ip(cls, request: HttpRequest) -> str:

        for header in cls.TRUSTED_HEADERS:
            ip = request.META.get(header)

            if ip:
                ip = ip.strip()

                if cls._is_valid_ip(ip):
                    return ip

        x_forwarded_for = request.META.get(
            "HTTP_X_FORWARDED_FOR",
            ""
        )

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
    # User Agent
    # ---------------------------------------------------------

    @staticmethod
    def get_user_agent(request: HttpRequest) -> str:
        return request.headers.get(
            "User-Agent",
            request.META.get(
                "HTTP_USER_AGENT",
                ""
            )
        )

    # ---------------------------------------------------------
    # Browser
    # ---------------------------------------------------------

    @classmethod
    def get_browser(cls, request: HttpRequest):

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
    def get_os(cls, request: HttpRequest):

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
    # Host
    # ---------------------------------------------------------

    @staticmethod
    def get_host(request: HttpRequest) -> str:
        return request.get_host()

    # ---------------------------------------------------------
    # Method
    # ---------------------------------------------------------

    @staticmethod
    def get_method(request: HttpRequest) -> str:
        return request.method

    # ---------------------------------------------------------
    # Referer
    # ---------------------------------------------------------

    @staticmethod
    def get_referer(request: HttpRequest) -> str:
        return request.headers.get(
            "Referer",
            request.META.get(
                "HTTP_REFERER",
                ""
            )
        )

    # ---------------------------------------------------------
    # RequestInfoModel
    # ---------------------------------------------------------

    @classmethod
    def get(cls, request: HttpRequest) -> HttpRequestMetadataModel:

        browser, browser_version = cls.get_browser(request)
        os_name, os_version = cls.get_os(request)

        return HttpRequestMetadataModel(
            ip_address=cls.get_client_ip(request),
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

'''import ipaddress
from django.http import HttpRequest
from user_agents import parse
from .request_info_model import RequestInfoModel

class RequestInfoProvider:

    TRUSTED_HEADERS = (
        "HTTP_CF_CONNECTING_IP",   # Cloudflare
        "HTTP_TRUE_CLIENT_IP",     # Cloudflare Enterprise / Akamai
        "HTTP_X_REAL_IP",          # Nginx
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

    @classmethod
    def get_client_ip(cls, request: HttpRequest) -> str:

        # 1. Trusted Proxy Headers
        for header in cls.TRUSTED_HEADERS:
            ip = request.META.get(header)

            if ip:
                ip = ip.strip()

                if cls._is_valid_ip(ip):
                    return ip

        # 2. X-Forwarded-For
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")

        if x_forwarded_for:
            for ip in x_forwarded_for.split(","):
                ip = ip.strip()

                if cls._is_valid_ip(ip):
                    return ip

        # 3. REMOTE_ADDR
        ip = request.META.get("REMOTE_ADDR", "")

        if cls._is_valid_ip(ip):
            return ip

        return ""

    @staticmethod
    def get_user_agent(request: HttpRequest) -> str:
        return request.headers.get(
            "User-Agent",
            request.META.get("HTTP_USER_AGENT", "")
        )

    @classmethod
    def _get_parsed_user_agent(cls, request: HttpRequest):
        """
        Parse User-Agent only once per request.
        """

        cache_name = "_parsed_user_agent"

        if not hasattr(request, cache_name):
            setattr(
                request,
                cache_name,
                parse(cls.get_user_agent(request))
            )

        return getattr(request, cache_name)

    @classmethod
    def get_browser(cls, request: HttpRequest) -> str:
        return cls._get_parsed_user_agent(request).browser.family

    @classmethod
    def get_browser_version(cls, request: HttpRequest) -> str:
        ua = cls._get_parsed_user_agent(request)
        return ".".join(map(str, ua.browser.version))

    @classmethod
    def get_os(cls, request: HttpRequest) -> str:
        return cls._get_parsed_user_agent(request).os.family

    @classmethod
    def get_os_version(cls, request: HttpRequest) -> str:
        ua = cls._get_parsed_user_agent(request)
        return ".".join(map(str, ua.os.version))

    @classmethod
    def get_device(cls, request: HttpRequest) -> str:
        return cls._get_parsed_user_agent(request).device.family

    @classmethod
    def get_device_brand(cls, request: HttpRequest) -> str:
        return cls._get_parsed_user_agent(request).device.brand or ""

    @classmethod
    def get_device_model(cls, request: HttpRequest) -> str:
        return cls._get_parsed_user_agent(request).device.model or ""

    @classmethod
    def get_device_type(cls, request: HttpRequest) -> str:

        ua = cls._get_parsed_user_agent(request)

        if ua.is_mobile:
            return "Mobile"

        if ua.is_tablet:
            return "Tablet"

        if ua.is_pc:
            return "Desktop"

        if ua.is_bot:
            return "Bot"

        return "Unknown"

    @staticmethod
    def get_host(request: HttpRequest) -> str:
        return request.get_host()

    @staticmethod
    def get_method(request: HttpRequest) -> str:
        return request.method

    @staticmethod
    def get_referer(request: HttpRequest) -> str:
        return request.headers.get(
            "Referer",
            request.META.get("HTTP_REFERER", "")
        )

    @classmethod
    def get(cls, request: HttpRequest) -> RequestInfoModel:

        return RequestInfoModel(
            ip_address=cls.get_client_ip(request),
            user_agent=cls.get_user_agent(request),

            browser=cls.get_browser(request),
            browser_version=cls.get_browser_version(request),

            os=cls.get_os(request),
            os_version=cls.get_os_version(request),

            device=cls.get_device(request),
            device_brand=cls.get_device_brand(request),
            device_model=cls.get_device_model(request),
            device_type=cls.get_device_type(request),

            host=cls.get_host(request),
            method=cls.get_method(request),
            referer=cls.get_referer(request),
        )'''
# Use: pip install user-agents