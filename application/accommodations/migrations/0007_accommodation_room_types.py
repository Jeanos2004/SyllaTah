# Generated by Django 5.1.6 on 2025-03-24 02:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0006_roomtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='room_types',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accommodations.roomtype'),
        ),
    ]
