import urllib.parse
import pymongo
from config import MONGO_USER, MONGO_PASSWORD


username = urllib.parse.quote_plus(MONGO_USER)
password = urllib.parse.quote_plus(MONGO_PASSWORD)

client = pymongo.MongoClient(f'mongodb://{username}:{password}@ds227459.mlab.com:27459/flats')
db = client['flats']

try:
    seen = pickle.load(open("seen.p", "rb"))
except:
    seen = set()

try:
    events_stack = pickle.load("events_stack.p", "rb")
except:
    events_stack = []


def update_data(text):
    seen.add(text)
    pickle.dump(seen, open("seen.p", "wb"))


def update_stack(text):
    events_stack.append(text)
    pickle.dump(seen, open("events_stack.p", "wb"))