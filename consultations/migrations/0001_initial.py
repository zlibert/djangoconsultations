# Generated by Django 3.1.1 on 2020-09-17 20:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('age', models.IntegerField(verbose_name='patient age')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('height', models.IntegerField(verbose_name='height in cm')),
                ('weight', models.IntegerField(verbose_name='weight in kg')),
                ('avg_waking_temp', models.FloatField(verbose_name='average waking temperature in centigrades')),
                ('avg_waking_pulse', models.IntegerField(verbose_name='average waking pulse')),
                ('avg_afternoon_temp', models.FloatField(verbose_name='average waking temperature in centigrades')),
                ('avg_afternoon_pulse', models.IntegerField(verbose_name='average afternoon pulse')),
                ('avg_sys_bp', models.IntegerField(verbose_name='average systolic blood pressure')),
                ('avg_dias_bp', models.IntegerField(verbose_name='average diastolic blood pressure')),
                ('bodyfat', models.FloatField(verbose_name='body fat percentage')),
                ('country', models.CharField(max_length=64, verbose_name='country of residence')),
                ('city', models.CharField(max_length=64, verbose_name='city of residence')),
                ('avg_artificial_light', models.IntegerField(verbose_name='average hours under artificial blue light')),
                ('avg_sleep_hours', models.FloatField(verbose_name='average hours of sleep per night')),
                ('avg_sleep_quality', models.CharField(choices=[('B', 'Bad'), ('R', 'Regular'), ('G', 'Good')], max_length=1, verbose_name='how patient feels after sleeping')),
                ('stresslevel', models.CharField(choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')], max_length=1, verbose_name='how stressed the patient feels')),
                ('workhours', models.IntegerField(verbose_name='how many hours does the patient regularly work per day')),
                ('previous_conditions', models.TextField()),
                ('family_history', models.TextField()),
                ('current_medications', models.TextField()),
                ('current_symptoms', models.TextField()),
                ('expectations', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=datetime.datetime.now, max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('filecontent', models.FileField(upload_to='media/uploads/')),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultations.consultation')),
            ],
        ),
    ]