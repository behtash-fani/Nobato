from django import forms
from professionals.models import StylistProfile
from .models import Availability
from django.contrib.auth.decorators import login_required

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['weekday', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

