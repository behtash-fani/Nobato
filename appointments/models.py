<<<<<<< HEAD
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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


class Appointment(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    professional_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    professional_object_id = models.PositiveIntegerField()
    professional = GenericForeignKey('professional_content_type', 'professional_object_id')
    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        indexes = [
            models.Index(fields=['professional_content_type', 'professional_object_id', 'date']),
            models.Index(fields=['customer', 'date']),
        ]

=======
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError


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

    professional_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    professional_object_id = models.PositiveIntegerField(null=True, blank=True)
    professional = GenericForeignKey('professional_content_type', 'professional_object_id')

    specific_date = models.DateField(null=True, blank=True, db_index=True)
    weekday = models.IntegerField(choices=WEEKDAYS, verbose_name="روز هفته", null=True, blank=True)

    start_time = models.TimeField(verbose_name="ساعت شروع")
    end_time = models.TimeField(verbose_name="ساعت پایان")

    class Meta:
        ordering = ['specific_date', 'weekday', 'start_time']
        indexes = [
            models.Index(fields=['professional_content_type', 'professional_object_id', 'specific_date']),
            models.Index(fields=['professional_content_type', 'professional_object_id', 'weekday']),
        ]
        verbose_name = "زمان آزاد"
        verbose_name_plural = "زمان‌های آزاد"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("ساعت پایان باید بعد از ساعت شروع باشد.")

        if not self.specific_date and self.weekday is None:
            raise ValidationError("یا تاریخ مشخص را پر کنید یا روز هفته را انتخاب کنید.")

        if self.specific_date and self.weekday is not None:
            raise ValidationError("Availability نمی‌تواند همزمان تاریخ مشخص و روز هفته داشته باشد.")

        base_qs = Availability.objects.filter(
            professional_content_type=self.professional_content_type,
            professional_object_id=self.professional_object_id,
        ).exclude(pk=self.pk)

        if self.specific_date:
            q = base_qs.filter(specific_date=self.specific_date)
        else:
            q = base_qs.filter(specific_date__isnull=True, weekday=self.weekday)

        overlapping = q.filter(start_time__lt=self.end_time, end_time__gt=self.start_time).exists()
        if overlapping:
            raise ValidationError("این بازه زمانی با بازه‌ی دیگری تداخل دارد.")

    def __str__(self):
        label = self.specific_date.isoformat() if self.specific_date else dict(self.WEEKDAYS).get(self.weekday, '?')
        return f"{label} {self.start_time}-{self.end_time} ({self.professional})"


class Booking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELED = 'canceled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELED, 'Canceled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')

    professional_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    professional_object_id = models.PositiveIntegerField()
    professional = GenericForeignKey('professional_content_type', 'professional_object_id')

    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['professional_content_type', 'professional_object_id', 'date', 'start_time', 'end_time'],
                name='unique_booking_slot',
            )
        ]
        indexes = [
            models.Index(fields=['professional_content_type', 'professional_object_id', 'date']),
            models.Index(fields=['customer', 'date']),
        ]
        ordering = ['date', 'start_time']
        verbose_name = "رزرو"
        verbose_name_plural = "رزروها"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("ساعت پایان باید بعد از ساعت شروع باشد.")

        py_weekday = self.date.weekday()          # Monday=0
        avail_weekday = (py_weekday + 1) % 7      # Saturday=0

        covering = Availability.objects.filter(
            professional_content_type=self.professional_content_type,
            professional_object_id=self.professional_object_id,
        ).filter(
            models.Q(specific_date=self.date) |
            models.Q(specific_date__isnull=True, weekday=avail_weekday)
        ).filter(
            start_time__lte=self.start_time,
            end_time__gte=self.end_time
        ).exists()

        if not covering:
            raise ValidationError("این بازه در دسترسی‌های متخصص پوشش داده نشده است.")

        overlapping = Booking.objects.filter(
            professional_content_type=self.professional_content_type,
            professional_object_id=self.professional_object_id,
            date=self.date,
        ).exclude(pk=self.pk).exclude(status=self.STATUS_CANCELED).filter(
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exists()
        if overlapping:
            raise ValidationError("این بازه با یک رزرو دیگر تداخل دارد.")
>>>>>>> 100bba5 (Inititial commit)
