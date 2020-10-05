from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Consultation(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    SLEEP_CHOICES = [('B', 'Bad'), ('R', 'Regular'), ('G', 'Good')]
    STRESSLEVEL_CHOICES = [('L', 'Low'), ('M', 'Medium'), ('H', 'High')]
    DEFECATION_CHOICES = [('<1', 'Less than one'), ('1', 'Once'), ('2', 'Twice'), ('3', 'Thrice'), ('>3', 'More than thrice')]
    STATUS_CHOICES = [('Open', 'Open'), ('Closed', 'Closed'), ('Resolved', 'Resolved'), ('Rejected', 'Rejected'), ('Pending', 'Pending'),
                      ('Waiting for Patient', 'Waiting for Patient'), ('Waiting for Payment', 'Waiting for Payment')]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations_created')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations_assigned', blank=True, null=True)

    timestamp = models.DateTimeField(default=datetime.now)
    age = models.IntegerField('Patient age')
    sex = models.CharField('Patient sex', max_length=1, choices=SEX_CHOICES)
    height = models.IntegerField('Height in cm')
    weight = models.IntegerField('Weight in kg')
    avg_waking_temp = models.FloatField('Average waking temperature in centigrades')
    avg_waking_pulse = models.IntegerField('Average waking pulse')
    avg_afternoon_temp = models.FloatField('Average afternoon temperature in centigrades')
    avg_afternoon_pulse = models.IntegerField('Average afternoon pulse')
    avg_sys_bp = models.IntegerField('Average systolic blood pressure')
    avg_dias_bp = models.IntegerField('Average diastolic blood pressure')
    bodyfat = models.FloatField('Body fat percentage')
    country = models.CharField('Country of residence', max_length=64)
    city = models.CharField('City of residence', max_length=64)
    avg_artificial_light = models.IntegerField('Average hours under artificial blue light')
    avg_sleep_hours = models.FloatField('Average hours of sleep per night')
    avg_sleep_quality = models.CharField('Energy level after sleeping', max_length=1, choices=SLEEP_CHOICES)
    stresslevel = models.CharField('Level of daily stress', max_length=1, choices=STRESSLEVEL_CHOICES)
    workhours = models.IntegerField('Work hours per day')
    bowelmovements = models.CharField('Average bowel movements per day', max_length=2, choices=DEFECATION_CHOICES, default='1')
    alcohol_use = models.TextField('Alcohol Consumption', blank=True)
    previous_conditions = models.TextField('Previous diagnosed conditions', blank=True)
    family_history = models.TextField('Family diagnosed conditions', blank=True)
    current_medications = models.TextField('Current drugs or medications', blank=True)
    current_symptoms = models.TextField('Current Symptoms', blank=True)
    expectations = models.TextField()

    status = models.CharField('Case status', max_length=32, choices=STATUS_CHOICES, default='Open')
    price = models.IntegerField('Price in USD', null=True)
    paymentinfo = models.TextField('Payment information', blank=True)


class UploadedFile(models.Model):
    # Uploaded files related to a Consultation - One to Many
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    filecontent = models.FileField('File', upload_to='uploads/')


class Message(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
