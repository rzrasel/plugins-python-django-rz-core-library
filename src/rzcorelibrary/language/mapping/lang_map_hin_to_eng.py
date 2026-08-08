# File Name: rz-core-libarary/src/rzcorelibrary/language/mapping/lang_map_hin_to_eng.py

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

class LangMapHinToEng(LanguageMapping):

    from_language = LanguageType.HINDI
    to_language = LanguageType.ENGLISH

    mapping: Dict[str, str] = {
        'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo',
        'ऋ': 'ri', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
        'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
        'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'nya',
        'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
        'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
        'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
        'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh', 'ष': 'sh', 'स': 's', 'ह': 'h',
        'ड़': 'r', 'ढ़': 'rh',
        'ा': 'a', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo', 'ृ': 'ri',
        'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', '्': '',
        'ं': 'n', 'ः': 'h', 'ँ': 'n', '़': '',
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9',
    }

    # conjuncts - must be checked before single chars
    conjuncts = {
        'क्ष': 'ksh', 'त्र': 'tr', 'ज्ञ': 'gya',
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
    def code_point_decimal_v_1_0_0(cls) -> Dict[str, str]:
        """Includes conjuncts: {'2329-2381-2359': 'ksh'}"""
        decimal_mapping: Dict[str, str] = {str(ord(k)): v for k, v in cls.mapping.items()}
        for k, v in cls.conjuncts.items():
            key = "-".join(str(ord(c)) for c in k)
            decimal_mapping[key] = v
        return decimal_mapping

    @classmethod
    def to_eng(cls, text: str) -> str:
        text = unicodedata.normalize('NFC', text)
        full = {**cls.conjuncts, **cls.mapping}
        keys = sorted(full.keys(), key=len, reverse=True)
        res = []
        i = 0
        while i < len(text):
            if text[i] in ('\u200c', '\u200d'):
                i += 1
                continue
            matched = False
            for k in keys:
                if text[i:].startswith(k):
                    if '\u0900' <= text[i] <= '\u097F':
                        res.append(full[k])
                    else:
                        res.append(text[i])
                    i += len(k)
                    matched = True
                    break
            if not matched:
                ch = text[i]
                res.append(cls.mapping.get(ch, '') if '\u0900' <= ch <= '\u097F' else ch)
                i += 1
        return "".join(res)

    @classmethod
    def translate(cls, text: str) -> str:
        return cls.to_eng(text)

class Plugin(BasePlugin):
    name = "lang_map_hin_to_eng"
    version = "1.0.0"
    def get_util(self):
        return LangMapHinToEng