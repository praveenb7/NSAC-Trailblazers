from time import sleep
from . import models
import pickle
import numpy as np
from django.core.mail import send_mail
from django.conf import settings

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


@shared_task()
def send_email_to_users(queryset):
    for query in queryset:
        email = query.user.email
        if email:
            try:
                send_email(email)
                pass
            except:
                pass

    return True


def send_email(email):
    subject = "Fire Alert"
    message = "Fire in your Area"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [email, ]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=to_email, fail_silently=True)
    return True
