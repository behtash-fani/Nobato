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
