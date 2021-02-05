import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import PIL
import tensorflow as tf

from PIL import Image
from pathlib import Path
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

data_dir = Path('/home/juan/Downloads/images/resized/')
image_count = len(list(data_dir.glob('*.jpg')))


images = list(data_dir.glob('*.jpg'))

batch_size = 3111
img_height = 300
img_width = 300

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

"""
for image in images:
    img = Image.open(image)
    new_img = img.resize((300, 300), Image.ANTIALIAS)
    path_name = "/home/juan/Downloads/images/resized/" + image.name
    new_img.save(path_name, "JPEG", quality=90)
"""


