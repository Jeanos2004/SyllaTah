# Generated by Django 5.1.6 on 2025-03-29 03:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodge', '0003_lodge_type_alter_lodge_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lodgeaccommodation',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lodgeactivity',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
