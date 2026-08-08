# File Name: rz-core-libarary/src/rzcorelibrary/language/mapping/lang_map_eng_to_ben.py

try:
    from plugins.base import BasePlugin
except ImportError:
    try:
        from ....plugins.base import BasePlugin
    except ImportError:
        BasePlugin = object

import unicodedata
from .language_mapping import LanguageMapping
from ..type.language_type import LanguageType

class LangMapEngToBen(LanguageMapping):
    from_language = LanguageType.ENGLISH
    to_language = LanguageType.BANGLA

    # reverse - digraphs must be checked first in translator
    mapping: Dict[str, str] = {
        # digraphs / trigraphs
        'kh': 'খ', 'gh': 'ঘ', 'ch': 'চ', 'chh': 'ছ', 'jh': 'ঝ',
        'th': 'থ', 'dh': 'ধ', 'ph': 'ফ', 'bh': 'ভ', 'sh': 'শ',
        'rh': 'ড়', 'ng': 'ং', 'ny': 'ঞ', 'nya': 'ঞ',
        'ee': 'ী', 'uu': 'ূ', 'oi': 'ৈ', 'ou': 'ৌ', 'ri': 'ৃ',
        # single
        'a': 'আ', 'i': 'ই', 'u': 'উ', 'e': 'এ', 'o': 'ও',
        'k': 'ক', 'g': 'গ', 'c': 'চ', 'j': 'য', 't': 'ত', 'd': 'দ', 'n': 'ন',
        'p': 'প', 'f': 'ফ', 'b': 'ব', 'v': 'ভ', 'm': 'ম',
        'y': 'য়', 'r': 'র', 'l': 'ল', 's': 'স', 'h': 'হ',
        'q': 'ক', 'Q': 'ক',
        '.': '।',
        '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯',
    }

    @classmethod
    def code_point_decimal(cls) -> Dict[int, str]:
        decimal_mapping: Dict[int, str] = {}
        for char, value in cls.mapping.items():
            if len(char) == 1:
                decimal_mapping[ord(char)] = value
            else:
                decimal_mapping[ord(char[0])] = value
        return decimal_mapping

    @classmethod
    def to_ben(cls, text: str) -> str:
        # longest match first for kh, chh etc
        result = []
        i = 0
        text = text.lower()
        sorted_keys = sorted(cls.mapping.keys(), key=len, reverse=True)
        while i < len(text):
            matched = False
            for k in sorted_keys:
                if text[i:i+len(k)] == k:
                    result.append(cls.mapping[k])
                    i += len(k)
                    matched = True
                    break
            if not matched:
                result.append(text[i])
                i += 1
        return "".join(result)

    @classmethod
    def translate(cls, text: str) -> str:
        return cls.to_ben(text)

class Plugin(BasePlugin):
    name = "lang_map_eng_to_ben"
    version = "1.0.0"
    def get_util(self):
        return LangMapEngToBen