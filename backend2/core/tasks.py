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
    if predict_by_iot_inputs(40, 50, 10):
        return True
    return False


@shared_task()
def predict_by_iot_inputs(oxygen, temperature, humidity):
    model = pickle.load(open('model.pkl', 'rb'))
    int_features = [oxygen, temperature, humidity] # [oxygen, temperature, humidity]
    final = [np.array(int_features)]
    prediction = model.predict_proba(final)
    output = '{0:.{1}f}'.format(prediction[0][1], 2)
    if int(output) >=0.5:
        return True
    return False


@shared_task()
def predict_by_image():
    return True
