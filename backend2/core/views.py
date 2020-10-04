from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import Distance as measureDistance
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from . import serializers
from . import models
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import tasks, forms
from django.core.files import File


# Create your views here.
def Home(request):
    return render(request, "index.html")


# Create your views here.
@login_required
def Dashboard(request):
    user = request.user
    userprofile = models.Profile.objects.get(user=user)
    context = {
        "user": user,
        "profile": userprofile,

    }
    return render(request, "user/dashboard.html", context)


@login_required
def NearbyFirestation(request):
    user = request.user
    userprofile = models.Profile.objects.get(user=user)

    firestations = models.FireStation.objects.all()
    firestations = firestations.annotate(distance=Distance("location", userprofile.location)).order_by('distance')

    context = {
        "user": user,
        "profile": userprofile,
        "firestations": firestations,

    }
    return render(request, "user/nearby_fire_stations.html", context=context)


@login_required
def NearbyRescueCenter(request):
    user = request.user
    userprofile = models.Profile.objects.get(user=user)

    rescuecenters = models.RescueCenter.objects.all()
    rescuecenters = rescuecenters.annotate(distance=Distance("location", userprofile.location)).order_by('distance')

    context = {
        "user": user,
        "profile": userprofile,
        "rescuecenters": rescuecenters,

    }
    return render(request, "user/nearby_rescue_centers.html", context=context)


@login_required
def NearbyFireReports(request):
    user = request.user
    userprofile = models.Profile.objects.get(user=user)

    fire_reports = models.RescueCenter.objects.all()
    fire_reports = fire_reports.annotate(distance=Distance("location", userprofile.location)).order_by('distance')[0:20]

    context = {
        "user": user,
        "profile": userprofile,
        "reports": fire_reports,
    }
    return render(request, "user/nearby_fire_reports.html", context=context)


@login_required
def ReportFire(request):
    user = request.user
    userprofile = models.Profile.objects.get(user=user)
    fire_reports = models.RescueCenter.objects.all()
    fire_reports = fire_reports.annotate(distance=Distance("location", userprofile.location)).order_by('distance')[0:20]

    if request.method == 'POST':
        form = forms.UserReportForm(request.POST, request.FILES)
        print(request.POST)
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        location = GEOSGeometry('SRID=4326;POINT(' + str(longitude) + ' ' + str(latitude) + ')')
        image = request.FILES['image']
        image = File(image)
        report = models.UserReport.objects.create(image=image, location=location, user=user, verified=False,
                                                  ongoing=False)
        rid = int(report.id)
        tasks.predict_by_image.delay(rid)
        return redirect("core:report")
    else:
        form = forms.UserReportForm()
    context = {
        "user": user,
        "profile": userprofile,
        "reports": fire_reports,
        "form": form,
    }
    return render(request, "user/report_fire.html", context=context)


@login_required
def ReviewFireReports(request):
    user = request.user
    userprofile = models.Profile.objects.get(user=user)
    fire_reports = models.RescueCenter.objects.all()
    fire_reports = fire_reports.annotate(distance=Distance("location", userprofile.location)).order_by('distance')[0:20]

    context = {
        "user": user,
        "profile": userprofile,
        "reports": fire_reports,
    }
    return render(request, "user/review_fire_reports.html", context=context)


@login_required
def CommunityForumView(request):
    user = request.user
    userprofile = models.Profile.objects.get(user=user)

    # all_users = models.Profile.objects.all()
    # all_users = all_users.annotate(distance=Distance("location", userprofile.location)).order_by('distance')[0:20]
    all_users = models.Profile.objects.filter(location__distance_lt=(userprofile.location, measureDistance(km=10)))

    context = {
        "user": user,
        "all_users": all_users,
        "profile": userprofile,
    }
    return render(request, "user/community_forum.html", context=context)


@login_required
def UserProfileView(request):
    user = request.user
    userprofile = models.Profile.objects.get(user=user)

    context = {
        "user": user,
        "profile": userprofile,
    }
    return render(request, "user/user_profile.html", context=context)


class IotDeviceAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        oxygen = request.data.get('oxygen' or None)
        temperature = request.data.get('temperature' or None)
        humidity = request.data.get('humidity' or None)
        latitude = request.data.get('latitude' or None)
        longitude = request.data.get('longitude' or None)
        image = request.data.get('image' or None)
        location = GEOSGeometry('SRID=4326;POINT(' + str(longitude) + ' ' + str(latitude) + ')')
        if image:
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            image = request.FILES['image']
            image = File(image)
            device_report = models.DeviceReports.objects.create(location=location, image=image, oxygen=oxygen,
                                                                temperature=temperature, humidity=humidity,
                                                                process_status=0, verified=False, ongoing=False)
        else:
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            device_report = models.DeviceReports.objects.create(location=location, oxygen=oxygen,
                                                                temperature=temperature, humidity=humidity,
                                                                process_status=0, verified=False, ongoing=False)
            # tasks.predict_by_iot_inputs(device_report.id)

        serializer = serializers.DeviceReportSerializer(device_report, many=False)
        return Response({"data": serializer.data})

    def get(self, request):
        return Response([], status=200)


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
            rescuecenters = rescuecenters.annotate(distance=Distance("location", ref_location)).order_by('distance')[
                            0:6]

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
