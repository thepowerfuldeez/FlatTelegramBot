import pymorphy2
from nltk.tokenize import RegexpTokenizer
import hashlib


# TODO: SQL timestamp and md5 hash record
def is_center_room(text, timestamp=None):
    tokens = RegexpTokenizer(r'[а-яА-Я]+').tokenize(text)
    morph = pymorphy2.MorphAnalyzer()
    lemmatized = [morph.parse(token)[0].normal_form for token in tokens]
    if "комната" in lemmatized:
        if {"центр", "владимирская", "достоевская", "сенная", "спасская", "садовая", "чернышевская", "звенигородская",
            "пушкинская"} & set(lemmatized):
            md5 = hashlib.md5("".join(lemmatized).encode()).hexdigest()
            return True
