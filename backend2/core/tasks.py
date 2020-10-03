from time import sleep
from . import models
import pickle
import numpy as np

from celery import shared_task

@shared_task()
def sleepy():
    sleep(10)
    return None

@shared_task()
def predict_fire():

    pass

@shared_task()
def predict_by_iot_inputs():
    model = pickle.load(open('model.pkl', 'rb'))
    int_features=[]     # [oxygen, temperature, humidity]

    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict_proba(final)
    output='{0:.{1}f}'.format(prediction[0][1], 2)
    return True

@shared_task()
def predict_by_image():
    return True