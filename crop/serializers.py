from crop.models import Crop, GrowthPlan, Tray
from rest_framework import serializers

class CropSerializer(serializers.ModelSerializer):
    """
    Serializer for the Crop model
    """

    def create(self, validated_data):
        crop = Crop(**validated_data)
        crop.save()

        return crop

    class Meta:
        model = Crop
        fields = ['id', 'name', 'family']

class GrowthPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the GrowthPlan model
    """

    def create(self, validated_data):
        growth_plan = GrowthPlan(**validated_data)
        growth_plan.save()

        return growth_plan

    class Meta:
        model = GrowthPlan
        fields = ['id', 'crop', 'name', 'growth_duration', 'est_yield']

class TraySerializer(serializers.ModelSerializer):
    """
    Serializer for the Tray model
    """
    def create(self, validated_data):
        tray = Tray(**validated_data)
        tray.save()

        return tray

    class Meta:
        model = Tray
        fields = ['id', 'crop', 'growth_plan', 'sow_date', 'harvest_date', 'total_yield']


