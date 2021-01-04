from time import sleep
from .models import UserReport
from . import models
import pickle
from django.core.mail import send_mail
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import Distance as measureDistance
from celery import shared_task
import tensorflow as tf
import numpy as np
from keras.preprocessing import image
from django.conf import settings
import os


@shared_task()
def classify(path):
    # test_image = Image.open(BytesIO(response.content))
    test_image = image.load_img(path, target_size=(150, 150))
    test_image2 = image.img_to_array(test_image)
    test_image2 = np.expand_dims(test_image2, axis=0)

    file_path = os.path.join(settings.STATIC_ROOT, 'colab.h5')
    model = tf.keras.models.load_model(file_path)
    try:
        res = model.predict(test_image2)
        result = res[0][0]
        return result
    except Exception as error:
        return False


@shared_task()
def sleepy():
    sleep(10)
    return None


@shared_task()
def predict_by_iot_inputs(did):
    device_report = models.DeviceReports.objects.get(id=did)
    oxygen = device_report.oxygen
    temperature = device_report.temperature
    humidity = device_report.humidity
    try:
        # url = staticfiles_storage.url('data/foobar.csv')
        file_path = os.path.join(settings.STATIC_ROOT, 'model.pkl')
        model = pickle.load(open(file_path, 'rb'))
        int_features = [oxygen, temperature, humidity] # [oxygen, temperature, humidity]
        final = [np.array(int_features)]
        prediction = model.predict_proba(final)
        output = '{0:.{1}f}'.format(prediction[0][1], 2)
        # print(output)
        if float(output) >=0.5:
            device_report.verified = True
            device_report.ongoing = True
            device_report.save()

            try:
                fire_reports = models.RescueCenter.objects.all()
                fire_reports = fire_reports.annotate(distance=Distance("location", device_report.location)).order_by(
                                'distance')[0:6]
                send_email_to_fire_stations(fire_reports)
            except:
                pass

            try:
                rescuecenters = models.RescueCenter.objects.all()
                rescuecenters = rescuecenters.annotate(distance=Distance("location", device_report.location)).order_by(
                                'distance')[0:6]
                send_email_to_rescue_centers(rescuecenters)
            except:
                pass

            try:
                all_users = models.Profile.objects.filter(
                    location__distance_lt=(device_report.location, measureDistance(km=10)))
                send_email_to_users(all_users)
            except:
                pass
            return True
    except Exception as error:
        pass
    return False


@shared_task()
def predict_by_image(rid):
    report = UserReport.objects.filter(id=rid, process_status=0)[0]
    user = report.user
    userprofile = models.Profile.objects.get(user=user)
    # print(settings.MEDIA_ROOT2)
    BASE_DIR = getattr(settings, "BASE_DIR", "/")
    # print(BASE_DIR)

    image_path = BASE_DIR + str(report.image.url)
    # image_path = os.path.join(BASE_DIR, report.image.url)

    # print(image_path)
    result = classify(image_path)

    if result == 1:
        report.verified = True
        report.ongoing = True
        report.save()
        fire_reports = models.RescueCenter.objects.all()
        fire_reports = fire_reports.annotate(distance=Distance("location", userprofile.location)).order_by('distance')[0:6]
        send_email_to_fire_stations(fire_reports)

        rescuecenters = models.RescueCenter.objects.all()
        rescuecenters = rescuecenters.annotate(distance=Distance("location", userprofile.location)).order_by(
                                                'distance')[0:6]
        send_email_to_rescue_centers(rescuecenters)

        all_users = models.Profile.objects.filter(location__distance_lt=(userprofile.location, measureDistance(km=10)))
        send_email_to_users(all_users)

        return True
    else:
        return False


@shared_task()
def send_email_to_users(queryset):
    for query in queryset:
        email = query.user.email
        if email:
            try:
                send_email_function(email)
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
                send_email_function(email)
                pass
            except:
                pass

    return True


@shared_task()
def send_email_to_rescue_centers(queryset):
    for query in queryset:
        email = query.user.email

        send_email_function(email)


def send_email_function(email):
    subject = "Fire Alert"
    message = "Fire in your Area"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [email, 'sanyam19092000@gmail.com']
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=to_email, fail_silently=True)
    return True
