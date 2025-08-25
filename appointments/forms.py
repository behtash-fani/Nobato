<<<<<<< HEAD
from django import forms
from professionals.models import StylistProfile
from .models import Availability, Appointment
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


class BookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['customer', 'date', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'form-control'
        self.fields['start_time'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['end_time'].widget = forms.TimeInput(attrs={'type': 'time'})
=======
from django import forms
from .models import Availability


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['specific_date', 'weekday', 'start_time', 'end_time']
        labels = {
            'specific_date': 'تاریخ مشخص',
            'weekday': 'روز هفته',
            'start_time': 'ساعت شروع',
            'end_time': 'ساعت پایان',
        }
        widgets = {
            'specific_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'weekday': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        specific_date = cleaned.get('specific_date')
        weekday = cleaned.get('weekday')

        if not specific_date and weekday is None:
            raise forms.ValidationError("یا تاریخ مشخص را پر کنید یا روز هفته را انتخاب کنید.")
        if specific_date and weekday is not None:
            raise forms.ValidationError("نمی‌توانید همزمان تاریخ مشخص و روز هفته را پر کنید.")
        return cleaned
>>>>>>> 100bba5 (Inititial commit)
