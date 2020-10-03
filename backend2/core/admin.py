from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.FireStation)
admin.site.register(models.RescueCenter)
admin.site.register(models.UserReport)
admin.site.register(models.DeviceReports)
admin.site.register(models.UserReportReview)