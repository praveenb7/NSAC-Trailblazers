from rest_framework.routers import DefaultRouter
from . import serializers, views

router = DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')
router.register('fire-station', views.FireStationViewSet, basename='fire-station')
router.register('rescue-center', views.RescueCenterViewSet, basename='rescue-center')
router.register('user-report', views.UserReportViewSet, basename='user-report')
router.register('device-report', views.DeviceReportViewSet, basename='device-report')
router.register('user-report-review', views.UserReportReviewViewSet, basename='user-report-review')
