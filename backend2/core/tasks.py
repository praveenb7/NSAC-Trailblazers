from time import sleep
from . import models
import pickle
import numpy as np
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import Distance as measureDistance


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
def predict_by_image(report):
    user = report.user
    userprofile = models.Profile.objects.get(user=user)
    result = True

    if result:
        fire_reports = models.RescueCenter.objects.all()
        fire_reports = fire_reports.annotate(distance=Distance("location", userprofile.location)).order_by('distance')[0:6]
        send_email_to_fire_stations(fire_reports)

        rescuecenters = models.RescueCenter.objects.all()
        rescuecenters = rescuecenters.annotate(distance=Distance("location", userprofile.location)).order_by(
                                                'distance')[0:6]
        send_email_to_rescue_centers(rescuecenters)

        all_users = models.Profile.objects.filter(location__distance_lt=(userprofile.location, measureDistance(km=10)))
        send_email(all_users)

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

@shared_task()
def send_email_to_fire_stations(queryset):
    for query in queryset:
        email = query.user.email
        if email:
            try:
                send_email(email)
                pass
            except:
                pass

    return True

@shared_task()
def send_email_to_rescue_centers(queryset):
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
