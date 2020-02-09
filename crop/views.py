from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
import json
from django.core.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from crop.models import Crop, GrowthPlan, Tray, OutputDevice
from crop.serializers import CropSerializer, TraySerializer, GrowthPlanSerializer
from rest_framework.decorators import api_view

# pylint: disable=all

class CropApi(APIView):

    def get(self, request):
        paginator = PageNumberPagination()
        crops = paginator.paginate_queryset(Crop.objects.all().order_by('id'), request)
        serializer = CropSerializer(crops, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CropSerializer(data=request.data)
        is_valid = serializer.is_valid()
        if is_valid == False:
             return Response({'status': 'failed', 'message': serializer.errors}, status=422)

        new_crop = serializer.save()

        return Response(serializer.data)

class GrowthPlanApi(APIView):

    def get(self, request):
        paginator = PageNumberPagination()
        growth_plans = paginator.paginate_queryset(GrowthPlan.objects.all().order_by('id'), request)
        serializer = GrowthPlanSerializer(growth_plans, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = GrowthPlanSerializer(data=request.data)
        is_valid = serializer.is_valid()
        if is_valid == False:
             return Response({'status': 'failed', 'message': serializer.errors}, status=422)

        new_growth_plan = serializer.save()

        return Response(serializer.data)

    @api_view(('POST',))
    def add_device(self, growth_plan_id, device_id):
       growth_plan = GrowthPlan.objects.get(id=growth_plan_id)
       growth_plan.output_devices.add(OutputDevice.objects.get(id=device_id))
       serializer = GrowthPlanSerializer(growth_plan)

       return Response(serializer.data)

class TrayApi(APIView):

    def get(self, request):
        paginator = PageNumberPagination()
        queryset = Tray.objects.all()

        if request.GET.get('crop_id') != None:
            queryset = queryset.filter(crop_id=request.GET.get('crop_id'))

        if request.GET.get('growth_plan_id') != None:
            queryset = queryset.filter(growth_plan_id=request.GET.get('growth_plan_id'))

        crops = paginator.paginate_queryset(queryset.order_by('id'), request)
        serializer = TraySerializer(crops, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TraySerializer(data=request.data)
        is_valid = serializer.is_valid()
        if is_valid == False:
             return Response({'status': 'failed', 'message': serializer.errors}, status=422)

        new_tray = serializer.save()

        return Response(serializer.data)
