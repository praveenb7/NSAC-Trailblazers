from django.urls import path, include
from . import views
app_name = 'core'


urlpatterns = [
    path('', views.Home, name='home'),
    path('fire-stations/', views.NearbyFirestation, name='fire-stations'),
    path('rescue-centers/', views.NearbyRescueCenter, name='rescue-centers'),
    path('fire-reports/', views.NearbyFireReports, name='fire-reports'),
    path('report/', views.ReportFire, name='report'),
    path('community/', views.CommunityForumView, name='community'),

]