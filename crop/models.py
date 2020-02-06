from django.db import models
import django
from django.core.validators import MaxLengthValidator, DecimalValidator

# pylint: disable=all


class Crop(models.Model):
    """
    A species of crop that can be grown in the farm
    """

    name = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])  # name of crop
    family = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])  # family of crop e.g. Basil


class GrowthPlan(models.Model):
    """
    the projected growth of a crop
    """

    crop = models.ForeignKey(Crop, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, validators=[MaxLengthValidator(50)])  # name of plan
    growth_duration = models.IntegerField()  # days
    est_yield = models.IntegerField()  # estimated yield grams


class Tray(models.Model):
    """
    A tray of crop that has been sown in the farm
    """

    crop = models.ForeignKey(Crop, on_delete=models.PROTECT)
    growth_plan = models.ForeignKey(
        GrowthPlan, on_delete=models.PROTECT)
    sow_date = models.DateTimeField(
        default=django.utils.timezone.now())  # date sown
    harvest_date = models.DateTimeField(
        default=None, null=True, blank=True)  # date harvested
    total_yield = models.IntegerField(default=0)  # amount harvested
    estimated_yield = models.IntegerField(default=None, null=True, blank=True)  # estimated yield grams
    estimated_harvest_date = models.DateTimeField(default=None, null=True, blank=True)  # estimated harvested