# File Name: rz-core-libarary/src/rzcorelibrary/utilities/string/string_utils.py

try:
    from plugins.base import BasePlugin
except ImportError:
    from ....plugins.base import BasePlugin

import re
import unicodedata
from typing import Any, Optional

from ...language.imports import (
    LanguageType,
    LanguageTranslator,
)

class StringUtils:

    def __init__(self):
        raise TypeError(
            f"{self.__class__.__name__} cannot be instantiated."
        )

    @staticmethod
    def to_escape_string(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        # MySQL escaping: \ first, then others
        if isinstance(value, bytes):
            return (
                value.replace(b"\\", b"\\\\")
                .replace(b"\0", b"\\0")
                .replace(b"\n", b"\\n")
                .replace(b"\r", b"\\r")
                .replace(b"\x1a", b"\\Z")
                .replace(b"'", b"\\'")
                .replace(b'"', b'\\"')
            )

        return (
            value.replace("\\", "\\\\")
            .replace("\0", "\\0")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\x1a", "\\Z")
            .replace("'", "\\'")
            .replace('"', '\\"')
        )

    @staticmethod
    def to_collapse_whitespace(value: Optional[str], strip: bool = True) -> Optional[str]:
        if value is None:
            return None
        collapsed: str = re.sub(r"\s+", " ", value)
        return collapsed.strip() if strip else collapsed

    @staticmethod
    def to_normalize_whitespace(value: Optional[str]) -> Optional[str]:
        return StringUtils.to_collapse_whitespace(value, strip=True)

    @staticmethod
    def to_squish(value: Optional[str]) -> Optional[str]:
        return StringUtils.to_collapse_whitespace(value, strip=True)

    @staticmethod
    def to_strip_whitespace(value: Optional[str]) -> Optional[str]:
        return StringUtils.to_collapse_whitespace(value, strip=True)

    @staticmethod
    def to_slug(
            value: Optional[str],
            lower: bool = True,
            allow_unicode: bool = True
    ) -> Optional[str]:
        if value is None:
            return None

        value = value.strip()
        if not value:
            return ""

        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            # Café -> Cafe
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')

        if lower:
            value = value.lower()

        # Replace anything not alphanumeric with -
        value = re.sub(r"[^\w\s-]", "", value)  # remove special chars
        value = re.sub(r"[\s_]+", "-", value)  # spaces/underscore -> -
        value = re.sub(r"-{2,}", "-", value)  # --- -> -

        return value.strip("-")

    @staticmethod
    def to_slug_translation(
            value: Optional[str],
            lower: bool = True,
            allow_unicode: bool = True,
            to_language: LanguageType = LanguageType.ENGLISH,
    ) -> Optional[str]:
        if value is None:
            return None

        translator: LanguageTranslator = LanguageTranslator()
        text: Optional[str] = translator.translate_to(
            text=value,
            to_language=to_language
        )

        return StringUtils.to_slug(
            value=text,
            lower=lower,
            allow_unicode=allow_unicode
        )

    @staticmethod
    def get_slug_number(value: str) -> Optional[int]:
        match = re.search(r"-(\d+)$", value)
        return int(match.group(1)) if match else None

    @staticmethod
    def is_empty(value: Any) -> bool:
        if value is None:
            return True

        if isinstance(value, str):
            return not value.strip()
        if isinstance(value, (list, dict, set, tuple)):
            return len(value) == 0

        return False

    @staticmethod
    def is_null(value: Any) -> bool:
        return value is None

    @staticmethod
    def is_all_empty(*values: Any) -> bool:
        # all() = AND
        # StringUtils.is_all_empty((raw_language_id, raw_language_slug))
        return all(StringUtils.is_empty(item) for item in values)

    @staticmethod
    def is_any_empty(*values: Any) -> bool:
        # any() = OR
        # StringUtils.is_any_empty((raw_language_id, raw_language_slug))
        return any(StringUtils.is_empty(item) for item in values)

    @staticmethod
    def parse_bool(value: Any, default: bool = False) -> bool:
        true_set = {"true", "1", "t", "yes", "y", "on"}
        false_set = {"false", "0", "f", "no", "n", "off", ""}

        if value is None:
            return default

        if isinstance(value, bool):
            return value

        if isinstance(value, int) and not isinstance(value, bool):
            if value == 1:
                return True
            if value == 0:
                return False
            return default

        if isinstance(value, str):
            v = value.strip().lower()
            if v in true_set:
                return True
            if v in false_set:
                return False
            return default

        return bool(value)

    @staticmethod
    def get_bool(value: Any) -> bool:
        if isinstance(value, str):
            return value.strip().lower() == "true"
        return bool(value)

    @staticmethod
    def _transliterate_bn(text: str) -> str:
        # Basic Bangla -> English mapping for slug
        mapping = {
            'অ': 'o', 'আ': 'a', 'ই': 'i', 'ঈ': 'ee', 'উ': 'u', 'ঊ': 'uu', 'ঋ': 'ri',
            'এ': 'e', 'ঐ': 'oi', 'ও': 'o', 'ঔ': 'ou',
            'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
            'চ': 'c', 'ছ': 'ch', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'nya',
            'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
            'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
            'প': 'p', 'ফ': 'ph', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
            'য': 'y', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh', 'স': 's', 'হ': 'h',
            'ড়': 'r', 'ঢ়': 'rh', 'য়': 'y', 'ৎ': 't',
            'া': 'a', 'ি': 'i', 'ী': 'ee', 'ু': 'u', 'ূ': 'uu', 'ৃ': 'ri',
            'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou', '্': '', 'ঁ': 'n', 'ং': 'ng', 'ঃ': 'h',
            '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9',
        }
        result = ""
        for ch in text:
            result += mapping.get(ch, ch)
        return result

class Plugin(BasePlugin):
    name = "string_utils"
    version = "1.0.0"
    description = "String escaping utility"
    def get_util(self):
        return StringUtils