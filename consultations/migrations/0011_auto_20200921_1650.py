# Generated by Django 3.1.1 on 2020-09-21 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consultations', '0010_auto_20200921_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultations_assigned', to=settings.AUTH_USER_MODEL),
        ),
    ]
