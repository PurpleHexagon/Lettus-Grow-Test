# Generated by Django 2.2 on 2020-02-07 17:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crop', '0005_auto_20200207_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='growthplan',
            name='output_devices',
            field=models.ManyToManyField(to='crop.OutputDevice'),
        ),
    ]
