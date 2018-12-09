import pickle

try:
    seen = pickle.load(open("seen.p", "rb"))
except:
    seen = set()


def update_data(text):
    seen.add(text)
    pickle.dump(seen, open("seen.p", "wb"))

events_stack = []
