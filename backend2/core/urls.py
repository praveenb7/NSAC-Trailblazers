from django.urls import path, include
from . import views
app_name = 'core'


urlpatterns = [
    path('', views.Home, name='home'),
    path('accounts/login/', views.Login, name='login'),
    path('accounts/logout/', views.Logout, name='logout'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('fire-stations/', views.NearbyFirestation, name='fire-stations'),
    path('rescue-centers/', views.NearbyRescueCenter, name='rescue-centers'),
    path('fire-reports/', views.NearbyFireReports, name='fire-reports'),
    path('report/', views.ReportFire, name='report'),
    path('review-reports/', views.ReviewFireReports, name='review-reports'),
    path('community/', views.CommunityForumView, name='community'),
    path('profile/', views.UserProfileView, name='profile'),
    path('device-api/', views.IotDeviceAPIView.as_view(), name='device-api'),

]