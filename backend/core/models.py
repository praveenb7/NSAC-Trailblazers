from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length = 16, blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True)


class FireStation(models.Model):
    user = models.ForeignKey('core.User', on_delete = models.CASCADE)
    name = models.CharField(max_length = 512)
    email = models.EmailField()
    mobile = models.CharField(max_length = 15)
    alternate_mobile = models.CharField(max_length = 15)
    location = models.PointField(srid=4326, geography=True)
    firetendors = models.PositiveSmallIntegerField()
    staff = models.ManytoManyField("core.User")



# @receiver(post_save, sender=User)
# def my_callback(sender, instance, *args, **kwargs):
#     user_subscription = UserSubscriptions.objects.get_or_create(user=instance)
#
