from django.urls import include, path
from crop import views
from rest_framework import routers

urlpatterns = [
    path('crop/', views.CropApi.as_view()),
    path('growthplan/', views.GrowthPlanApi.as_view()),
    path('tray/', views.TrayApi.as_view()),
]
