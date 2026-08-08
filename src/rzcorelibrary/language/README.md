### Build Plugin Rz Core Library:

```bash
python -c "import sys; sys.path.insert(0,'src'); from rzcorelibrary.language.transliterate.language_translator import LanguageTranslator; from rzcorelibrary.language.type.language_type import LanguageType; t=LanguageTranslator(); print(t.translate_to('অমর', LanguageType.ENGLISH)); print(t.translate_to('नमस्ते', LanguageType.ENGLISH))"
```

```bash
$str = "যয়য য়য্‌ বাংলায় squish শব্দের অর্থ হলো চেপে ধরা, চিপে ফেলা বা নরম কিছু চাপ দিয়ে ভেঙে ফেলা। এছাড়া ভেজা বা নরম কিছুর ওপর পা ফেলার সময় যে ঝুপঝুপ বা ছপছপ শব্দ হয়, তাকেও squish বলা হয়।";

$str = "আমার des হয় eta";

for ($i = 0; $i < mb_strlen($str, "UTF-8"); $i++) {
    $char = mb_substr($str, $i, 1, "UTF-8");
    echo "char: " . $char . " ord: " . ord($char) . " hex: " . bin2hex($char) . " ";
}

$str = "আমার des হয় eta";

for ($i = 0; $i < mb_strlen($str, "UTF-8"); $i++) {
    $char = mb_substr($str, $i, 1, "UTF-8");
    $codepoint = mb_ord($char, "UTF-8");
    echo "char: " . $char . " ord: " . $codepoint . " hex: U+" . dechex($codepoint) . " bin2hex: " . bin2hex($char) . " ";
}

- convert in python
- provide full code


python -c "import sys; sys.path.insert(0,'src'); from rzcorelibrary.language.transliterate.language_translator import LanguageTranslator; from rzcorelibrary.language.type.language_type import LanguageType; t=LanguageTranslator(); print(t.translate_to('যয়য য়য্‌ বাংলায় squish শব্দের অর্থ হলো চেপে ধরা, চিপে ফেলা বা নরম কিছু চাপ দিয়ে ভেঙে ফেলা। এছাড়া ভেজা বা নরম কিছুর ওপর পা ফেলার সময় যে ঝুপঝুপ বা ছপছপ শব্দ হয়, তাকেও squish বলা হয়।', LanguageType.ENGLISH)); print(t.translate_to('नमस्ते', LanguageType.ENGLISH))"
python -c "import sys; sys.path.insert(0,'src'); from rzcorelibrary.language.transliterate.language_translator import LanguageTranslator; from rzcorelibrary.language.type.language_type import LanguageType; t=LanguageTranslator(); print(t.translate_to('আমার des হয় eta', LanguageType.ENGLISH))"
python -c "import sys; sys.path.insert(0,'src'); from rzcorelibrary.language.transliterate.language_translator import LanguageTranslator; from rzcorelibrary.language.type.language_type import LanguageType; t=LanguageTranslator(); print(t.translate_to('শব্দের', LanguageType.ENGLISH))"
python -c "import sys; sys.path.insert(0,'src'); from rzcorelibrary.language.transliterate.language_translator import LanguageTranslator; from rzcorelibrary.language.type.language_type import LanguageType; t=LanguageTranslator(); print(t.translate_to('हिमाचल प्रदेश में पेट्रोल और हाई-स्पीड डीजल पर 'अनाथ और विधवा सेस' बढ़ा दिया गया है. यह फैसला बुधवार रात 12 बजे से लागू होगा, जिसके बाद पेट्रोल और डीज.', LanguageType.ENGLISH))"
```

```bash
python -c "import sys; sys.path.insert(0,'src'); from rzcorelibrary.language.transliterate.language_translator import LanguageTranslator; from rzcorelibrary.language.type.language_type import LanguageType; t=LanguageTranslator(); print(t.translate_to('बढ़ा दिया गया है. यह फैसला बुधवार रात 12 बजे से लागू होगा, जिसके बाद पेट्रोल और डीज.', LanguageType.ENGLISH))"
```
