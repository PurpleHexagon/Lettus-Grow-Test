from django.contrib import admin

from .models import Crop, GrowthPlan, Tray, OutputDevice, OutputDeviceScheduledTask

admin.site.register(Crop)
admin.site.register(GrowthPlan)
admin.site.register(Tray)
admin.site.register(OutputDevice)
admin.site.register(OutputDeviceScheduledTask)
