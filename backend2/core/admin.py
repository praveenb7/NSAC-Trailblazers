from django.contrib import admin
from . import models
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

class ProfileAdmin(LeafletGeoAdmin):
    pass

class FireStationAdmin(LeafletGeoAdmin):
    pass

class RescueCenterAdmin(LeafletGeoAdmin):
    pass

class UserReportAdmin(LeafletGeoAdmin):
    pass

class DeviceReportAdmin(LeafletGeoAdmin):
    pass

class UserReportReviewAdmin(LeafletGeoAdmin):
    pass

admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.FireStation, FireStationAdmin)
admin.site.register(models.RescueCenter, RescueCenterAdmin)
admin.site.register(models.UserReport, UserReportAdmin)
admin.site.register(models.DeviceReports, DeviceReportAdmin)
admin.site.register(models.UserReportReview, UserReportReviewAdmin)