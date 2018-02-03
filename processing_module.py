import pymorphy2
from nltk.tokenize import RegexpTokenizer
import hashlib

tokenizer = RegexpTokenizer(r'[а-яА-Я0-9]+|[0-9.,]+')
morph = pymorphy2.MorphAnalyzer()
wanted_metro_stations = {"технологический", "звенигородская", "спасская", "сенная", "садовая", "чернышевская",
                         "восстание", "лиговский", "владимирская", "достоевская", "маяковская", "пушкинская"}
hardcoded_mistakes = {"том": "тысяча", "тр": "тысяча", "метр": "метро", "мина": "минута",
                      "ряд": "рядом", "далее": "дом"}  # pymorphy mistakes
price_regexp = r'(?<![0-9])[0-9.,]{2,5}\s*(рубль|тысяча|[0-9]{3}(?![0-9])|ку?(?!.))'
# Regular expression for getting good price value


def process_text(text, verbose=0):
    tokens = tokenizer.tokenize(text)
    lemmatized = list(map(lambda word: hardcoded_mistakes.get(word, word),  # replacing word from dict if exists
                          (morph.parse(token)[0].normal_form for token in tokens)))
    if "комната" in lemmatized and "хостел" not in lemmatized:
        if wanted_metro_stations & set(lemmatized):
            md5 = hashlib.md5(" ".join(lemmatized).encode()).hexdigest()
            if verbose:
                return " ".join(lemmatized)
            return md5
    return ""

