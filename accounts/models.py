from django.contrib.auth.models import AbstractUser
from django.db import models
from professionals.models import Job

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'مشتری'),
        ('professional', 'متخصص'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def profile(self):
        if hasattr(self, 'stylistprofile'):
            return self.stylistprofile
        if hasattr(self, 'doctorprofile'):
            return self.doctorprofile

