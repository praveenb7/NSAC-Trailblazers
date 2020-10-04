from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# Create your models here.

# class User(AbstractUser):
#     mobile = models.CharField(max_length = 16, blank=True, null=True)
#     profile_pic = models.ImageField(blank=True, null=True)
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    pic = models.ImageField(default='user pics/pic.webp', upload_to='user pics', blank=True, null=True)
    mobile = models.CharField(max_length=15)
    location = models.PointField(srid=4326, geography=True)


class FireStation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=512)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    alternate_mobile = models.CharField(max_length=15)
    location = models.PointField(srid=4326, geography=True)
    address = models.TextField(default='', blank=True, null=True)
    firetendors = models.PositiveSmallIntegerField()
    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="staff"
    )


class RescueCenter(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=512)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    alternate_mobile = models.CharField(max_length=15)
    location = models.PointField(srid=4326, geography=True)
    address = models.TextField(default='', blank=True, null=True)
    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="rescue_staff"
    )
    residents = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="residents"
    )


class UserReport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    location = models.PointField(srid=4326, geography=True)
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)
    process_status = models.SmallIntegerField(default=0)
    verified = models.BooleanField(default=False)


class DeviceReports(models.Model):
    location = models.PointField(srid=4326, geography=True)
    image = models.ImageField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    process_status = models.SmallIntegerField(default=0)
    verified = models.BooleanField(default=False)


class UserReportReview(models.Model):
    report = models.ForeignKey(
        'core.UserReport',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    valid = models.BooleanField()
