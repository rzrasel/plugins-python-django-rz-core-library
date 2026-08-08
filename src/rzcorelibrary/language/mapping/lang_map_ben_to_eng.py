# File Name: rz-core-libarary/src/rzcorelibrary/language/mapping/lang_map_ben_to_eng.py

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

class LangMapBenToEng(LanguageMapping):
    from_language = LanguageType.BANGLA
    to_language = LanguageType.ENGLISH

    mapping: Dict[str, str] = {
        'অ': 'o', 'আ': 'a', 'ই': 'i', 'ঈ': 'ee', 'উ': 'u', 'ঊ': 'uu', 'ঋ': 'ri',
        'এ': 'e', 'ঐ': 'oi', 'ও': 'o', 'ঔ': 'ou',
        'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
        'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'nya',
        'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
        'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
        'প': 'p', 'ফ': 'f', 'ব': 'b', 'ভ': 'v', 'ম': 'm',
        'য': 'j', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh', 'স': 's', 'হ': 'h',
        'ড়': 'r', 'ঢ়': 'rh', 'য়': 'y', 'ৎ': 't',
        'া': 'a', 'ি': 'i', 'ী': 'ee', 'ু': 'u', 'ূ': 'uu', 'ৃ': 'ri',
        'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou', '্': '', 'ঁ': 'n', 'ং': 'ng', 'ঃ': 'h', '।': '.', '়': '',
        '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9',
    }

    # hex_mapping = {f"\\u{ord(k):04x}": v for k, v in mapping.items()}

    # All possible encodings of য়
    extra = {
        '\u09df': 'y', # য় single
        '\u09af\u09bc': 'y', # য + nukta
        '\u09af\u09cd\u09af': 'y', # য + hasant + য
        '\u09af\u200d': 'y', # য + ZWJ
        '\u09df\u200d': 'y',
        '\u09af\u09cd': 'y',
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

    '''@classmethod
    def code_point_decimal(cls) -> Dict[int, str]:
        return {ord(k): v for k, v in cls.mapping.items()}'''

    @classmethod
    def to_eng(cls, text: str) -> str:

        result = []
        for i in range(len(text)):
            char = text[i]
            hex_char = f"\\u{ord(char):04x}"
            if ord(char) == 2527 or hex_char == "\u09df":
                result.append('y')
            else:
                result.append(cls.mapping.get(char, char))
            result.append(f"{ord(char)}")
        return "".join(result)

    @classmethod
    def translate(cls, text: str) -> str:
        return cls.to_eng(text)

    '''@staticmethod
    def transliterate(text: str) -> str:
    
        result = ""
        for ch in text:
            result += mapping.get(ch, ch)

        return result'''

    @classmethod
    def to_eng_v_1_0_1(cls, text: str) -> str:
        text = unicodedata.normalize('NFC', text)
        full = {**cls.extra, **cls.mapping}
        # longest first
        keys = sorted(full.keys(), key=len, reverse=True)

        res = []
        i = 0
        while i < len(text):
            # skip ZWJ/ZWNJ
            if text[i] in ('\u200c', '\u200d'):
                i += 1
                continue
            found = False
            for k in keys:
                if text[i:].startswith(k):
                    ch0 = text[i]
                    if '\u0980' <= ch0 <= '\u09FF':
                        res.append(full[k])
                    else:
                        res.append(ch0)
                    i += len(k)
                    found = True
                    break
            if not found:
                ch = text[i]
                if '\u0980' <= ch <= '\u09FF':
                    res.append(cls.mapping.get(ch, ''))  # unknown bangla -> '' not 'য়'
                else:
                    res.append(ch)
                i += 1
        return "".join(res)

    @classmethod
    def code_point_decimal_v_1_0_0(cls) -> Dict[int, str]:
        decimal_mapping: Dict[int, str] = {}
        for char, value in cls.mapping.items():
            if len(char) == 1:
                decimal_mapping[ord(char)] = value
            else:
                decimal_mapping[ord(char[0])] = value
        return decimal_mapping

class Plugin(BasePlugin):
    name = "lang_map_ben_to_eng"
    version = "1.0.0"
    def get_util(self):
        return LangMapBenToEng