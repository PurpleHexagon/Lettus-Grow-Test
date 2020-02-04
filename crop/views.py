from rest_framework.views import APIView
from rest_framework.response import Response
#import django_filters
import json

from crop.models import Crop, GrowthPlan, Tray

# pylint: disable=all


class CropApi(APIView):

    def get(self, request):
        data = []
        for crop in Crop.objects.all():
            data.append({
                'name': crop.name,
                'family': crop.family
            })

        return Response(data)

    def post(self, request):
        new_crop = Crop.objects.create(**request.data)
        new_crop.save()

        return Response({
            'name': new_crop.name,
            'family': new_crop.family
        })


class GrowthPlanApi(APIView):

    def get(self, request):
        data = []
        for growth_plan in GrowthPlan.objects.all():
            data.append({
                'crop_id': growth_plan.crop.id,
                'name': growth_plan.name,
                'growth_duration': growth_plan.growth_duration,
                'est_yield': growth_plan.est_yield
            })

        return Response(data)

    def post(self, request):
        new_growth_plan = GrowthPlan.objects.create(**request.data)
        new_growth_plan.save()
        return Response({
            'crop_id': new_growth_plan.crop.id,
            'name': new_growth_plan.name,
            'growth_duration': new_growth_plan.growth_duration,
            'est_yield': new_growth_plan.est_yield
        })


class TrayApi(APIView):

    def get(self, request):
        data = []
        for tray in Tray.objects.all():
            data.append({
                'crop_id': tray.crop.id,
                'growth_plan_id': tray.growth_plan.id,
                'sow_date': str(tray.sow_date),
                'harvest_date': str(tray.harvest_date),
                'total_yield': tray.total_yield,
            })

        return Response(data)

    def post(self, request):
        tray = Tray.objects.create(**request.data)
        tray.save()
        return Response({
            'crop_id': tray.crop_id,
            'growth_plan_id': tray.growth_plan_id,
            'sow_date': str(tray.sow_date),
            'harvest_date': str(tray.harvest_date),
            'total_yield': tray.total_yield,
        })
