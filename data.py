import urllib.parse
import urllib.request
import pymongo
from config import MONGO_USER, MONGO_PASSWORD


IMG_PATH = "models/real/"

username = urllib.parse.quote_plus(MONGO_USER)
password = urllib.parse.quote_plus(MONGO_PASSWORD)

client = pymongo.MongoClient(f'mongodb://{username}:{password}@ds227459.mlab.com:27459/flats')
db = client['flats']


def check_duplicates(text):
    return db.flats.find({"text": text}).limit(1).count() == 0


def save_img(link):
    path = IMG_PATH + link.rsplit("/", 1)[-1]
    _ = urllib.request.urlretrieve(link, path)
    return path


if __name__ == "__main__":
    print("current count", db.flats.find({}).count())
    db.flats.remove({})
    print("current count", db.flats.find({}).count())
