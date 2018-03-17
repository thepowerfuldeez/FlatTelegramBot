import pymorphy2
import re
from nltk.tokenize import RegexpTokenizer
import hashlib

MAX_PRICE = 16  # 16 thousand as we are truncating strings via re

tokenizer = RegexpTokenizer(r'[а-яА-Я0-9]+|[0-9.,]+')
morph = pymorphy2.MorphAnalyzer()
wanted_metro_stations = {"александр", "обводный", "фрунзенская", "ворота", "электросила", "нарвская",
                         "электросила", "парк"}
hardcoded_mistakes = {"том": "тысяча", "тр": "тысяча", "метр": "метро", "мина": "минута",
                      "ряд": "рядом", "далее": "дом", "хостела": "хостел"}  # pymorphy mistakes
price_regexp = r'(?<![0-9])([0-9.,]{4,5}|[0-9.,]{2})\s*(рубль|тысяча|[0-9]{3}(?![0-9])|к(?!.))'
# Regular expression for getting good price value


def utility_price(match):
    try:
        if isinstance(match, str):
            return int(match[:2])
        else:
            return int(match[0][:2])
    except ValueError:
        return 0


def lemmatize(text):
    tokens = tokenizer.tokenize(text)
    lemmatized = list(map(lambda word: hardcoded_mistakes.get(word, word),  # replacing word from dict if exists
                          (morph.parse(token)[0].normal_form for token in tokens)))
    return lemmatized


def md5_hash(s):
    return hashlib.md5(s.encode()).hexdigest()


def process_text_vk(text, verbose=0):
    lemmatized = lemmatize(text)
    if "комната" in lemmatized and "квартира" in lemmatized and "хостел" not in lemmatized \
            and "сосед" not in lemmatized:
        if wanted_metro_stations & set(lemmatized):
            s = " ".join(lemmatized)
            all_matches = re.findall(price_regexp, s) + ['0']
            price = max(map(utility_price, all_matches))  # if all_matches is empty then 0
            if price <= MAX_PRICE:
                if verbose:
                    return s
                return md5_hash(s)
    return ""


def process_text_avito(text):
    lemmatized = lemmatize(text)
    if lemmatized:
        s = " ".join(lemmatized)
        return md5_hash(s)
    return ""
