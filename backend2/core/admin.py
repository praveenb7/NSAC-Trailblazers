from django.contrib import admin
from . import models
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

class ProfileAdmin(LeafletGeoAdmin):
    pass

admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.FireStation)
admin.site.register(models.RescueCenter)
admin.site.register(models.UserReport)
admin.site.register(models.DeviceReports)
admin.site.register(models.UserReportReview)