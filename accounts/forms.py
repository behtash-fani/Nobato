<<<<<<< HEAD
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from professionals.models import Job
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'role', 'job', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['job'].queryset = Job.objects.order_by('title')
        self.fields['job'].required = False

        # اضافه کردن کلاس form-control به همه فیلدها
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
=======
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser
from professionals.models import Job


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'role', 'job', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in ('password1', 'password2'):
                field.widget.attrs.update({'class': 'form-control'})
            elif name == 'role':
                field.widget.attrs.update({'class': 'form-select'})
            elif name == 'job':
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class CustomLoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class JobSelectForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['job']
        labels = {'job': 'انتخاب شغل'}
        widgets = {
            'job': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job'].queryset = Job.objects.order_by('title')
        self.fields['job'].required = True
>>>>>>> 100bba5 (Inititial commit)
