# Generated by Django 5.1.6 on 2025-03-24 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='regions/assets'),
        ),
    ]
