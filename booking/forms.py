from .models import Appointment
from django import forms

class BookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['professional', 'date', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['professional'].queryset = StylistProfile.objects.all()
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['start_time'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['end_time'].widget = forms.TimeInput(attrs={'type': 'time'})
