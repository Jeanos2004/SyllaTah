# Generated by Django 5.1.6 on 2025-03-28 12:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodge', '0002_remove_lodgeadmin_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lodge',
            name='type',
            field=models.CharField(choices=[('hotel', 'Hotel'), ('resort', 'Resort'), ('guesthouse', 'Guest House')], default='hotel', max_length=50),
        ),
        migrations.AlterField(
            model_name='lodge',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lodge',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lodge',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='lodge',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
