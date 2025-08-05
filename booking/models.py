from django.db import models
from accounts.models import CustomUser
from professionals.models import StylistProfile


class Appointment(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    professional = models.ForeignKey(StylistProfile, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"نوبت برای {self.customer.username} با {self.professional.user.username} در {self.date} ساعت {self.start_time}"
