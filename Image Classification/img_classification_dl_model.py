#Making new Predictions

import tensorflow as tf
import numpy as np
from keras.preprocessing import image

def classify(path):
  test_image = image.load_img(path, target_size=(150,150))
  test_image2 = image.img_to_array(test_image)
  test_image2 = np.expand_dims(test_image2,axis=0)
  model = tf.keras.models.load_model('/content/drive/My Drive/Dataset/colab.h5')
  res = model.predict_proba(test_image2)
  return res[0]


'''
Testing the model with sample images
Note : [1. 0.] means fire, [0. 1.] means non fire. It is an numpy array with datatype float32

a = classify('/content/fire.634.png') #fire image
print(a)

Output :- [1. 0.] 

b = classify('/content/non_fire.182.png') #non fire image
print(b)

Output :- [0. 1.]

'''
