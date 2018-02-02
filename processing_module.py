import pymorphy2
from nltk.tokenize import RegexpTokenizer
import hashlib

tokenizer = RegexpTokenizer(r'[а-яА-Я]+')
morph = pymorphy2.MorphAnalyzer()


# TODO: SQL timestamp and md5 hash record
def process_text(text):
    tokens = tokenizer.tokenize(text)
    lemmatized = [morph.parse(token)[0].normal_form for token in tokens]
    if "комната" in lemmatized and "хостел" not in lemmatized:
        if {"центр", "владимирская", "достоевская", "сенная", "спасская", "садовая", "чернышевская", "звенигородская",
                "пушкинская"} & set(lemmatized):
            md5 = hashlib.md5(" ".join(lemmatized).encode()).hexdigest()
            return md5
    return ""

