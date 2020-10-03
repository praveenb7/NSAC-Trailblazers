from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import Distance
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from . import models
import datetime


class ProfileSerializer(GeoFeatureModelSerializer):
    # location = PointField()
    # fire_stations = serializers.SerializerMethodField(read_only=True)
    # rescue_centre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Profile
        geo_field = "location"
        fields = "__all__"

    def get_fire_stations(self, obj):
        firestations = models.FireStation.objects.all()
        latitude = obj.location.lat
        longitude = obj.location.lng

        ref_location = GEOSGeometry('SRID=4326;POINT(' + str(longitude) + ' ' + str(latitude) + ')')
        firestations = firestations.annotate(distance=Distance("location", ref_location)).order_by('distance')[0:6]
        serializer = FireStationSerializer(firestations, many=True)
        return serializer.data

    def get_rescue_centre(self, obj):
        firestations = models.FireStation.objects.all()
        return obj.location
        firestations = firestations.annotate(distance=Distance("location", obj.location)).order_by('distance')[0:6]
        print(firestations)
        serializer = FireStationSerializer(firestations, many=True)
        return serializer.data


class FireStationSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = models.FireStation
        fields = "__all__"

class RescueCenterSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = models.RescueCenter
        fields = "__all__"

class UserReportSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = models.UserReport
        fields = "__all__"

class DeviceReportSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = models.DeviceReports
        fields = "__all__"

class UserReportReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserReportReview
        fields = "__all__"


