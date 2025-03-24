# Generated by Django 5.1.6 on 2025-03-11 20:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryAccommodation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='accommodation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='accommodations/assets'),
        ),
        migrations.AlterField(
            model_name='accommodation',
            name='location',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='accommodation',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='accommodation',
            name='price_per_night',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=10),
        ),
        migrations.AddField(
            model_name='accommodation',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accommodations.categoryaccommodation'),
        ),
    ]
