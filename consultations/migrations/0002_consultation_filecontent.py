# Generated by Django 3.1.1 on 2020-09-17 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='filecontent',
            field=models.FileField(blank=True, upload_to='', verbose_name='optional upload file'),
        ),
    ]
