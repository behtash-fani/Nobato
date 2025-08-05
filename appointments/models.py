from django.db import models
from accounts.models import CustomUser
from professionals.models import StylistProfile


class Availability(models.Model):
    WEEKDAYS = [
        (0, 'شنبه'),
        (1, 'یکشنبه'),
        (2, 'دوشنبه'),
        (3, 'سه‌شنبه'),
        (4, 'چهارشنبه'),
        (5, 'پنجشنبه'),
        (6, 'جمعه'),
    ]

    stylist = models.ForeignKey(StylistProfile, on_delete=models.CASCADE, related_name='availabilities')
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField(verbose_name="ساعت شروع")
    end_time = models.TimeField(verbose_name="ساعت پایان")

    class Meta:
        unique_together = ('stylist', 'weekday', 'start_time', 'end_time')
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f"{self.stylist.user.username} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"
