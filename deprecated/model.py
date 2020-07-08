from fastai.basics import *
from fastai.vision import *
import pathlib
import pandas as pd
import torch as t
from torchvision import transforms as T
from PIL import Image

path = pathlib.Path("models")
neg = get_image_files(path/"negative_samples")
true = get_image_files(path/"true_samples")
df = pd.DataFrame({"name": neg+true,
                   "label":[0]*len(neg)+[1]*len(true)})
data = ImageDataBunch.from_df(".", df, ds_tfms=get_transforms(), size=224, bs=8
                                ).normalize(imagenet_stats)
learn = create_cnn(data, models.resnet34, metrics=error_rate)
# learn.fit_one_cycle(12, max_lr=5e-3)
# learn.unfreeze()
# learn.fit_one_cycle(8, max_lr=slice(1e-8,5e-6))
# learn.save("/home/george/workspace/FlatTelegramBot/models/model")
# learn.load("model")

model = learn.model
model.load_state_dict(t.load("/home/george/workspace/FlatTelegramBot/models/model.pth")['model'])
model.eval()

tfm = T.Compose([T.CenterCrop(224), T.ToTensor(), T.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])

def get_prediction(img_path):
    cls = model(tfm(Image.open(img_path)).unsqueeze(0).cuda()).argmax().item()
    return cls