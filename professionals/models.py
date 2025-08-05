from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import os
from django.utils.translation import gettext_lazy as _

ALLOWED_JOB_CODES = [
    'stylist',         # آرایشگر
    'doctor',         # پزشک
    'coach',          # مربی ورزشی
    'mechanic',       # مکانیک
    'lawyer',         # وکیل
    'designer',       # طراح
    'developer',      # برنامه‌نویس
    'electrician',    # برق‌کار
    'plumber',        # لوله‌کش
    'psychologist',   # روانشناس
]

class Job(models.Model):
    code = models.SlugField(
        max_length=50,
        unique=True,
        help_text="stylist, doctor, coach, mechanic, lawyer, designer, developer, electrician, plumber, psychologist",
    )
    title = models.CharField(
        max_length=100,
        verbose_name="عنوان فارسی شغل"
    )

    def __str__(self):
        return self.title

    def clean(self):
        if self.code not in ALLOWED_JOB_CODES:
            raise ValidationError(f"کد '{self.code}' مجاز نیست. از لیست معتبر استفاده کنید.")


def stylist_image_path(instance, filename):
    return f'{instance.user.job.code}/{instance.user.id}/profile.jpg'

class StylistProfile(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to=stylist_image_path,
        blank=True,
        null=True,
        verbose_name="عکس پروفایل"
    )
    salon_name = models.CharField(max_length=100, blank=True, verbose_name="نام سالن")
    experience_years = models.PositiveIntegerField(verbose_name="سال سابقه")
    specialty_description = models.TextField(blank=True, verbose_name="توضیحات تخصص")

    def __str__(self):
        return f"استایلیست: {self.user.username}"

