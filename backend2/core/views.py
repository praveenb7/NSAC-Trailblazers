from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import Distance
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from . import serializers
from . import models
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import tasks

# Create your views here.

def Home(request):
    tasks.sleepy.delay()
    return render(request, "index.html")
    # return redirect()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self, pk=None):
        if pk:
            profile = models.Profile.objects.get(id=pk)
        else:
            profile = models.Profile.objects.all()
        return profile

    def create(self, request, *args, **kwargs):
        data = self.request.data
        id = self.request.user.id
        user = models.Profile.objects.get(id=id)

        data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *arg, **kwargs):
        queryset = models.Profile.objects.all()
        serializer = serializers.ProfileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FireStationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FireStationSerializer

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [permissions.IsAuthenticated]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]

    def get_queryset(self, pk=None):
        if pk:
            firestations = models.FireStation.objects.get(id=pk)
        else:
            firestations = models.FireStation.objects.all()

        latitude = self.request.query_params.get('latitude' or None)
        longitude = self.request.query_params.get('longitude' or None)
        if latitude and longitude:
            ref_location = GEOSGeometry('SRID=4326;POINT(' + str(longitude) + ' ' + str(latitude) + ')')
            firestations = firestations.annotate(distance=Distance("location", ref_location)).order_by('distance')[0:6]

        return firestations


class RescueCenterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RescueCenterSerializer

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [permissions.IsAuthenticated]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]

    def get_queryset(self, pk=None):
        if pk:
            rescuecenters = models.RescueCenter.objects.get(id=pk)
        else:
            rescuecenters = models.RescueCenter.objects.all()

        latitude = self.request.query_params.get('latitude' or None)
        longitude = self.request.query_params.get('longitude' or None)
        if latitude and longitude:
            ref_location = GEOSGeometry('SRID=4326;POINT(' + str(longitude) + ' ' + str(latitude) + ')')
            rescuecenters = rescuecenters.annotate(distance=Distance("location", ref_location)).order_by('distance')[0:6]

        return rescuecenters


class UserReportViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserReportSerializer

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [permissions.IsAuthenticated]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]

    def get_queryset(self, pk=None):
        if pk:
            userreport = models.UserReport.objects.get(id=pk)
        else:
            userreport = models.UserReport.objects.all()
        return userreport

    # def create(self, request, *args, **kwargs):
    #     data = self.request.data
    #     id = self.request.user.id
    #     user = models.Profile.objects.get(id=id)
    #
    #     data['user'] = user.id
    #     serializer = self.get_serializer(data=self.request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeviceReportViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DeviceReportSerializer

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [permissions.IsAuthenticated]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]

    def get_queryset(self, pk=None):
        if pk:
            devicereport = models.DeviceReports.objects.get(id=pk)
        else:
            devicereport = models.DeviceReports.objects.all()
        return devicereport


class UserReportReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DeviceReportSerializer

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [permissions.IsAuthenticated]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]

    def get_queryset(self, pk=None):
        if pk:
            userreport = models.UserReportReview.objects.get(id=pk)
        else:
            userreport = models.UserReportReview.objects.all()
        return userreport
