# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser
from professionals.models import StylistProfile, DoctorProfile

JOB_PROFILE_MODEL = {
    'stylist': StylistProfile,
    'doctor' : DoctorProfile,
}

@receiver(post_save, sender=CustomUser)
def ensure_correct_profile(sender, instance: CustomUser, created, **kwargs):
    if instance.role != 'professional' or not instance.job:
        return

    job_code = instance.job.code
    ProfileModel = JOB_PROFILE_MODEL.get(job_code)
    if not ProfileModel:
        return

    for model in JOB_PROFILE_MODEL.values():
        if model is not ProfileModel:
            model.objects.filter(user=instance).delete()

    ProfileModel.objects.get_or_create(user=instance)
