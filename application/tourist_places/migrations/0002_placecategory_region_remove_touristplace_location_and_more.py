# Generated by Django 5.1.6 on 2025-03-25 05:26

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourist_places', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='places/categories/')),
            ],
            options={
                'verbose_name_plural': 'Place Categories',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='regions/')),
            ],
        ),
        migrations.RemoveField(
            model_name='touristplace',
            name='location',
        ),
        migrations.AddField(
            model_name='touristplace',
            name='accessibility',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='best_visit_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='contact_info',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='facilities',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='place_type',
            field=models.CharField(blank=True, choices=[('historical', 'Site Historique'), ('natural', 'Site Naturel'), ('cultural', 'Site Culturel'), ('religious', 'Site Religieux'), ('entertainment', 'Divertissement')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='total_reviews',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='touristplace',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='touristplace',
            name='image',
            field=models.ImageField(null=True, upload_to='tourist_places/'),
        ),
        migrations.AlterField(
            model_name='touristplace',
            name='opening_hours',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='touristplace',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourist_places.region'),
        ),
        migrations.CreateModel(
            name='PlaceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField()),
                ('visit_date', models.DateField()),
                ('photos', models.ImageField(blank=True, null=True, upload_to='place_reviews/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='tourist_places.touristplace')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('place', 'user')},
            },
        ),
    ]
