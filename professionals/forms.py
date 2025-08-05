from django import forms
from .models import StylistProfile

class StylistProfileForm(forms.ModelForm):
    class Meta:
        model = StylistProfile
        fields = ['profile_image', 'salon_name', 'experience_years', 'specialty_description']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'salon_name': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'specialty_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

