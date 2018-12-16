import pymorphy2
import re
from nltk.tokenize import RegexpTokenizer
import hashlib

MAX_PRICE = 35  # 35 thousand as we are truncating strings via re

tokenizer = RegexpTokenizer(r'[а-яА-Я0-9]+|[0-9.,]+')
morph = pymorphy2.MorphAnalyzer()
wanted_metro_stations = {'беговой', 'приморский', 'василеостровский', 'чкаловский', 'спортивный', 'садовый', 'чёрный',
                         'речка', 'петроградский', 'горьковский', 'сенной', 'площадь', 'фрунзенский', 'спасский', 'лесной',
                         'выборгский', 'площадь', 'ленин'}
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


def process_text_vk(text):
    lemmatized = lemmatize(text)
    if "сосед" not in lemmatized:
        if wanted_metro_stations & set(lemmatized):
            s = " ".join(lemmatized)
            all_matches = re.findall(price_regexp, s) + ['0']
            price = max(map(utility_price, all_matches))  # if all_matches is empty then 0
            if price <= MAX_PRICE:
                return s
    return ""


def process_text_avito(text):
    lemmatized = lemmatize(text)
    if lemmatized:
        s = " ".join(lemmatized)
        return s
    return ""


if __name__ == "__main__":
    print(lemmatize("беговая приморская василеостровская чкаловская спортивная садовая черная речка петроградская"
                    " горьковская сенная площадь фрунзенская спасская лесная выборгская площадь ленина"))
