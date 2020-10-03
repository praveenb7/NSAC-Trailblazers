from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length = 16, blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True)






# @receiver(post_save, sender=User)
# def my_callback(sender, instance, *args, **kwargs):
#     user_subscription = UserSubscriptions.objects.get_or_create(user=instance)
#
