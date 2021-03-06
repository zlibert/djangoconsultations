# Generated by Django 3.1.1 on 2020-09-17 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0005_auto_20200917_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='paymentinfo',
            field=models.TextField(blank=True, verbose_name='Payment information'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='price',
            field=models.IntegerField(null=True, verbose_name='Price in USD'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Resolved', 'Resolved'), ('Rejected', 'Rejected'), ('Pending', 'Pending'), ('Waiting for Patient', 'Waiting for Patient'), ('Waiting for Payment', 'Waiting for Payment')], default='Open', max_length=32, verbose_name='Case status'),
        ),
    ]
