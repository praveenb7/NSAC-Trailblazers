from rest_framework import serializers

from . import models
import datetime


class FireStationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FireStation
        fields = "__all__"

class RescueCenterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RescueCenter
        fields = "__all__"

class UserReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserReport
        fields = "__all__"

class DeviceReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DeviceReports
        fields = "__all__"

class UserReportReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserReportReview
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Profile
        fields = "__all__"
