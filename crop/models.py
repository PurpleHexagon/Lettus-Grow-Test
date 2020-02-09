from django.db import models
import django
from django.core.validators import MaxLengthValidator, DecimalValidator, RegexValidator
from datetime import datetime, date
from decimal import Decimal

# pylint: disable=all

class Crop(models.Model):
    """
    A species of crop that can be grown in the farm a
    """

    name = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])  # name of crop
    family = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])  # family of crop e.g. Basil

class OutputDevice(models.Model):
    """
    An output device such as a grow light
    """

    # TODO: Move these two an appropriate place, as these would change over time should be in database
    COST_PER_MILLILITRE = '0.0005' # Cost in pound
    COST_PER_KILOWATT = '0.0002' # Cost in pounds

    TYPE_GROW_LIGHT = 1
    TYPE_WATER_SPRAYER = 2
    TYPE_GROW_LIGHT_DESCRIPTION = 'Grow Light'
    TYPE_WATER_SPRAYER_DESCRIPTION = 'Water Sprayer'
    TYPES = ((TYPE_GROW_LIGHT, TYPE_GROW_LIGHT_DESCRIPTION), (TYPE_WATER_SPRAYER, TYPE_WATER_SPRAYER_DESCRIPTION))

    UNIT_MILLILITRES = 1
    UNIT_KILOWATTS = 2
    UNIT_MILLILITRES_DESCRIPTION = 'Millilitres'
    UNIT_KILOWATTS_DESCRIPTION = 'Kilowatts'
    UNITS = ((UNIT_MILLILITRES, UNIT_MILLILITRES_DESCRIPTION), (UNIT_KILOWATTS, UNIT_KILOWATTS_DESCRIPTION))

    name = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])  # name of device
    device_type = models.IntegerField(choices=TYPES) # The type of the device represented by an integer, 1: Grow Light
    units = models.IntegerField(choices=UNITS) # The units for the device
    units_per_second = models.IntegerField() # Units per second outputted

    def cost_per_unit(self):
        """
        Returns the correct unit type based on the device type
        """
        if self.device_type == self.UNIT_MILLILITRES:
            return Decimal(self.COST_PER_MILLILITRE)

        if self.device_type == self.UNIT_KILOWATTS:
            return Decimal(self.COST_PER_KILOWATT)

    def cost_per_day(self):
        """
        Calculates the cost per day by iterating through the devices and calculating the cost for each device
        TODO: Optimise by adding caching
        """

        cost_per_day = 0
        output_device_tasks = self.output_device_tasks.all()
        for output_device_task in output_device_tasks:
            delta = datetime.combine(date.min, output_device_task.end_time) - datetime.combine(date.min, output_device_task.start_time)
            cost_per_day = (Decimal(delta.total_seconds()) * self.units_per_second * self.cost_per_unit()) + cost_per_day

        return cost_per_day.quantize(Decimal("0.01"))

    def units_per_day(self):
        """
        Calculates the units per day by iterating through the devices and calculating the units used for each device
        TODO: Optimise by adding caching
        """

        units_per_day = 0
        output_device_tasks = self.output_device_tasks.all()
        for output_device_task in output_device_tasks:
            delta = datetime.combine(date.min, output_device_task.end_time) - datetime.combine(date.min, output_device_task.start_time)
            units_per_day = (Decimal(delta.total_seconds()) * Decimal(self.units_per_second)) + units_per_day

        return Decimal(units_per_day)

class OutputDeviceScheduledTask(models.Model):
    """
    A scheduled task for a device

    TODO: Currently a scheduled task only has a start and end time, this could be improved by also having the option
    of a duration and interval, ie turn on for 3 minutes at 15 minute intervals
    """

    output_device = models.ForeignKey(OutputDevice, on_delete=models.PROTECT, related_name='output_device_tasks')
    start_time = models.TimeField(default=None, null=False) # The start time of the task
    end_time = models.TimeField(default=None, null=True, blank=True) # The end time of the task

class GrowthPlan(models.Model):
    """
    the projected growth of a crop
    """

    crop = models.ForeignKey(Crop, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, validators=[MaxLengthValidator(50)])  # name of plan
    growth_duration = models.IntegerField()  # days
    est_yield = models.IntegerField()  # estimated yield grams
    output_devices = models.ManyToManyField(OutputDevice)

    @property
    def estimated_grow_cost(self):
        """
        Returns the estimated cost of resources for the grow plan
        """

        cost = Decimal('0')
        output_devices = self.output_devices.all()
        for output_device in output_devices:
            cost = cost + (output_device.cost_per_day() * self.growth_duration)
        return cost.quantize(Decimal("0.01"))

    @property
    def estimated_water_usage(self):
        """
        Returns the estimated water usage for the grow plan
        """

        water_used = Decimal('0')
        output_devices = self.output_devices.all()
        for output_device in output_devices:
            if output_device.device_type == OutputDevice.TYPE_WATER_SPRAYER:
                water_used = water_used + (output_device.units_per_day() * self.growth_duration)
        return water_used.quantize(Decimal("0.01"))

    @property
    def estimated_electricity_usage(self):
        """
        Returns the estimated electricity usage for the grow plan
        """

        electricity_used = Decimal('0')
        output_devices = self.output_devices.all()
        for output_device in output_devices:
            if output_device.device_type == OutputDevice.TYPE_GROW_LIGHT:
                electricity_used = electricity_used + (output_device.units_per_day() * self.growth_duration)
        return electricity_used.quantize(Decimal("0.01"))

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

    @property
    def grow_cost(self):
        """
        Returns the total cost of resources to grow the tray. This will return zero until there is a
        harvest_date and a sow_date
        """

        cost = Decimal('0')
        growth_plan = self.growth_plan

        if self.harvest_date == None or self.sow_date == None:
            return cost

        days_for_grow = self.harvest_date - self.sow_date
        output_devices = growth_plan.output_devices.all()

        for output_device in output_devices:
            cost = cost + (output_device.cost_per_unit() * output_device.units_per_day()) * ((Decimal(days_for_grow.total_seconds()) / 60 / 60) / 24)
        return cost.quantize(Decimal("0.01"))

    @property
    def water_used(self):
        """
        Returns the total water used to grow the tray. This will return zero until there is a
        harvest_date and a sow_date
        TODO: Add return an estimated usage when tray has not been harvested
        """

        growth_plan = self.growth_plan
        water_used = Decimal('0')

        if self.harvest_date == None or self.sow_date == None:
            return water_used

        days_for_grow = self.harvest_date - self.sow_date
        output_devices = growth_plan.output_devices.all()

        for output_device in output_devices:
            if output_device.device_type == OutputDevice.TYPE_WATER_SPRAYER:
                water_used = water_used + (output_device.units_per_day() * (Decimal((days_for_grow.total_seconds()) / 60 / 60) / 24))

        return water_used.quantize(Decimal("0.01"))

    @property
    def electricity_used(self):
        """
        Returns the total electricity used to grow the tray. This will return zero until there is a
        harvest_date and a sow_date
        TODO: Add return an estimated usage when tray has not been harvested
        """

        growth_plan = self.growth_plan
        electricity_used = Decimal('0')

        if self.harvest_date == None or self.sow_date == None:
            return electricity_used

        days_for_grow = self.harvest_date - self.sow_date
        output_devices = growth_plan.output_devices.all()

        for output_device in output_devices:
            if output_device.device_type == OutputDevice.TYPE_GROW_LIGHT:
                electricity_used = electricity_used + (output_device.units_per_day() * ((Decimal(days_for_grow.total_seconds()) / 60 / 60) / 24))

        return electricity_used.quantize(Decimal("0.01"))