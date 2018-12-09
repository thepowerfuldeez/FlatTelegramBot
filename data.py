import pickle

try:
    events = pickle.load(open("events.p", "rb"))
except:
    events = set()


def update_data(text):
    events.add(text)
    pickle.dump(events, open("events.p", "wb"))