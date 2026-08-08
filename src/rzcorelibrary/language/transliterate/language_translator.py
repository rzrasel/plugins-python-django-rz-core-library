# File Name: rz-core-libarary/src/rzcorelibrary/language/transliterate/language_translator.py

from __future__ import annotations

try:
    from plugins.base import BasePlugin
except ImportError:
    try:
        from ....plugins.base import BasePlugin
    except ImportError:
        BasePlugin = object

import unicodedata
from typing import Type, Optional, Dict, List

from ..type.language_type import LanguageType

from ..mapping.language_mapping import LanguageMapping

from ..mapping.lang_map_ben_to_eng import LangMapBenToEng
from ..mapping.lang_map_hin_to_eng import LangMapHinToEng
from ..mapping.lang_map_eng_to_ben import LangMapEngToBen

class LanguageTranslator:
    # Language Transliterator

    def __init__(self, src_map: Optional[Type[LanguageMapping]] = None):
        self.src_map = src_map
        self.language_list: List[Type[LanguageMapping]] = [
            LangMapBenToEng,
            LangMapHinToEng,
            LangMapEngToBen,
        ]

    def _get_reverse(self, map_cls: Type[LanguageMapping]) -> Dict[str, str]:
        if map_cls is None:
            raise ValueError("Language map is required.")

        # LangMapBenToEng.mapping = {'অ': 'o',...}
        # reverse = {'o': 'অ',...}
        reverse: Dict[str, str] = {}
        for native, foreign in map_cls.mapping.items():
            if foreign and foreign not in reverse:
                reverse[foreign] = native
        return reverse

    def translate(
            self,
            text: Optional[str],
            src_map: Optional[Type[LanguageMapping]] = None,
            is_reverse: bool = False
    ) -> Optional[str]:

        if text is None:
            return None

        text = unicodedata.normalize('NFC', text)

        if src_map is None and self.src_map is None:
            raise ValueError("Source language map is required.")

        if src_map is None:
            src_map = self.src_map

        if is_reverse:
            reverse = self._get_reverse(src_map)
            return "".join(reverse.get(ch, ch) for ch in text)

        translated_text = src_map.to_eng(text)

        return translated_text

    def transliterate(self, text: Optional[str]) -> Optional[str]:

        if text is None:
            return None

        text = unicodedata.normalize('NFC', text)

        if self.src_map is None:
            raise ValueError("Source language map not set in initialization.")
        return self.src_map.to_eng(text)

    def _get_char_property(self, text: Optional[str]) -> Optional[str]:

        if text is None:
            return None

        chars = []
        for i in range(len(text)):
            char = text[i]
            # chars.append(char)
            code_point = ord(char)
            # u_hex_char = f"\\u{code_point:04x}"
            chars.append(f"{char}-{code_point}")
            '''if ord(char) == 2527 or char == r"\u09df":
                print(f"extra char found: {hex_char}")'''
            # print(f"{char} -> {hex(ord(char))} -> {ord(char)}")
            # print(f"char: {char} u-hex: {u_hex_char} hex: {hex(code_point)} ord: {code_point}")
            # print(f"char: {ascii(char)} u-hex: {u_hex_char} ord: {code_point}")

        new_text = ", ".join(chars)
        # print(new_text)

        return new_text.strip()

    def translate_to(
            self,
            text: Optional[str],
            to_language: LanguageType,
    ) -> Optional[str]:

        if text is None:
            return None

        text = unicodedata.normalize('NFC', text)

        # map list variable
        '''language_maps: List[Type[LanguageMapping]] = [
            LangMapBenToEng,
            LangMapHinToEng,
        ]'''

        # marge all language map in a list where to_language = to_language
        '''filtered_maps = [
            m for m in language_maps
            if getattr(m, 'to_language', getattr(m, 'meta_to', None)) == to_language
        ]'''

        # return self._get_char_property(text)

        # marge all language map in a list where to_language = to_language
        filtered_maps = [
            m for m in self.language_list
            if m.to_language == to_language
        ]

        if not filtered_maps:
            raise ValueError(f"No language map found for target: {to_language}")

        # merge
        merged_mapping: Dict[str, str] = {}
        for map_cls in filtered_maps:
            # merged_mapping.update(map_cls.mapping)
            merged_mapping.update(map_cls.code_point_decimal())

        result = []
        for i in range(len(text)):
            char = text[i]
            # u_hex_char = f"\\u{ord(char):04x}"
            # direct compare
            code_point = ord(char)
            '''# Bangla Bengali
            if code_point == 2527:  # য়
                result.append('y')
            elif code_point == 2524:  # ড়
                result.append('r')
            elif code_point == 2404:  # ।
                result.append('.')
            elif code_point in (8204, 8205, 8203):  # ZWNJ, ZWJ
                # result.append('')
                continue
            else:
                # result.append(merged_mapping.get(char, char))
                result.append(merged_mapping.get(code_point, char))'''

            result.append(merged_mapping.get(code_point, char))
            #result.append(f"{ord(char)}")

        # translate text to to_language
        # return "".join(merged_mapping.get(ch, ch) for ch in text)
        return "".join(result)

class Plugin(BasePlugin):
    name = "language_translator"
    version = "1.0.0"
    def get_util(self):
        return LanguageTranslator