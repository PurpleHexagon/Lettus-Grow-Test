from django.urls import path
from crop import views

urlpatterns = [
    path('crop/', views.CropApi.as_view()),
    path('growthplan/', views.GrowthPlanApi.as_view()),
    path('tray/', views.TrayApi.as_view()),
]
