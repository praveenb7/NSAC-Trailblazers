"""backend2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core import views as core_views
# from core.routers import router
from rest_framework.routers import DefaultRouter
from core import serializers, views

router = DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')
router.register('fire-station', views.FireStationViewSet, basename='fire-station')
router.register('rescue-center', views.RescueCenterViewSet, basename='rescue-center')
router.register('user-report', views.UserReportViewSet, basename='user-report')
router.register('device-report', views.DeviceReportViewSet, basename='device-report')
router.register('user-report-review', views.UserReportReviewViewSet, basename='user-report-review')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.Home, name='home'),
    path('api/', include(router.urls), name='api'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)