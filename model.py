from fastai.basics import *
from fastai.vision import *

learn = Learner.load("model")

def get_prediction(img):
    learn.predict(img)