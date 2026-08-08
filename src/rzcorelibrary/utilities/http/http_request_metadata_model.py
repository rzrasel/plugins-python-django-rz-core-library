# File Name: rz-core-libarary/src/rzcorelibrary/utilities/http/http_request_metadata_model.py

from __future__ import annotations

try:
    from plugins.base import BasePlugin
except ImportError:
    from ....plugins.base import BasePlugin

from dataclasses import dataclass, asdict
from typing import Optional
import json

@dataclass(frozen=True)
class HttpRequestMetadataModel:

    # |----------------NETWORK INFORMATION----------------|
    ip_address: str
    host_ip: str
    host: str

    # |----------------CLIENT INFORMATION-----------------|
    user_agent: str
    device_type: str

    # |----------------BROWSER INFORMATION----------------|
    browser: str
    browser_version: str

    # |--------------OPERATING SYSTEM INFO----------------|
    os: str
    os_version: str

    # |----------------REQUEST INFORMATION----------------|
    method: str
    referer: str

    def __init__(
            self,
            ip_address: str,
            host_ip: str,
            host: str,
            user_agent: str,
            device_type: str,
            browser: str,
            browser_version: str,
            os: str,
            os_version: str,
            method: str,
            referer: str,
    ):
        object.__setattr__(self, "ip_address", ip_address)
        object.__setattr__(self, "host_ip", host_ip)
        object.__setattr__(self, "host", host)
        object.__setattr__(self, "user_agent", user_agent)
        object.__setattr__(self, "device_type", device_type)
        object.__setattr__(self, "browser", browser)
        object.__setattr__(self, "browser_version", browser_version)
        object.__setattr__(self, "os", os)
        object.__setattr__(self, "os_version", os_version)
        object.__setattr__(self, "method", method)
        object.__setattr__(self, "referer", referer)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(
        self,
        *,
        indent: Optional[int] = None,
        ensure_ascii: bool = False
    ) -> str:
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=ensure_ascii
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_json(cls, json_string: str):
        return cls.from_dict(json.loads(json_string))

class Plugin(BasePlugin):
    name = "http_request_metadata_model"
    version = "1.0.0"
    description = "HTTP request metadata model"

    def get_util(self):
        return HttpRequestMetadataModel