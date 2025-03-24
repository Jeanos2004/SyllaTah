# Generated by Django 5.1.6 on 2025-02-11 17:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accommodations', '0001_initial'),
        ('activities', '0001_initial'),
        ('transports', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateField(blank=True, null=True)),
                ('check_out_date', models.DateField(blank=True, null=True)),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
                ('accommodation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accommodations.accommodation')),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activities.activity')),
                ('transport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transports.transport')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
