from django.contrib import admin

from .models import Crop, GrowthPlan, Tray

admin.site.register(Crop)
admin.site.register(GrowthPlan)
admin.site.register(Tray)
