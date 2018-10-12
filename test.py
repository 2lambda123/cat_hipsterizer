import keras, sys, cv2, os
from keras.models import Model, load_model
import numpy as np
import pandas as pd

img_size = 224
base_path = 'samples'
file_list = sorted(os.listdir(base_path))

model_name = sys.argv[1]
model = load_model(model_name)

def resize_img(im):
  old_size = im.shape[:2] # old_size is in (height, width) format
  ratio = float(img_size) / max(old_size)
  new_size = tuple([int(x*ratio) for x in old_size])
  # new_size should be in (width, height) format
  im = cv2.resize(im, (new_size[1], new_size[0]))
  delta_w = img_size - new_size[1]
  delta_h = img_size - new_size[0]
  top, bottom = delta_h // 2, delta_h - (delta_h // 2)
  left, right = delta_w // 2, delta_w - (delta_w // 2)
  new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,
      value=[0, 0, 0])
  return new_im, ratio, top, left

for f in file_list:
  if '.jpg' not in f:
    continue

  img = cv2.imread(os.path.join(base_path, f))

  # resize image and relocate landmarks
  img, ratio, top, left = resize_img(img)

  inputs = (img.astype('float32') / 255).reshape((1, img_size, img_size, 3))
  bb = model.predict(inputs)[0].reshape((-1, 2))

  cv2.rectangle(img, pt1=tuple(bb[0]), pt2=tuple(bb[1]), color=(255, 255, 255), thickness=2)
  cv2.imshow('img', img)

  if cv2.waitKey(0) == ord('q'):
    break