import pickle

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