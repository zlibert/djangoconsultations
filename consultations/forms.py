from django import forms
from .models import Consultation


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = [
            'age',
            'sex',
            'height',
            'weight',
            'avg_waking_temp',
            'avg_waking_pulse',
            'avg_afternoon_temp',
            'avg_afternoon_pulse',
            'avg_sys_bp',
            'avg_dias_bp',
            'bodyfat',
            'country',
            'city',
            'avg_artificial_light',
            'avg_sleep_hours',
            'avg_sleep_quality',
            'stresslevel',
            'workhours',
            'bowelmovements',
            'previous_conditions',
            'family_history',
            'current_medications',
            'current_symptoms',
            'expectations'
        ]
