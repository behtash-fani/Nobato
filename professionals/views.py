<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import StylistProfileForm
from .models import StylistProfile
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import StylistProfile, Job
from appointments.models import Availability
from appointments.forms import AvailabilityForm
from .models import StylistProfile, DoctorProfile


def profile_view(request, profile_type, profile_id):
    profiles = {
        'stylist': StylistProfile,
        'doctor': DoctorProfile,
    }
    profile_model = profiles.get(profile_type)
    profile = get_object_or_404(profile_model, id=profile_id)
    return render(request, f'professionals/{profile_type}_profile.html', {'profile': profile})


def job_list(request):
    jobs = Job.objects.all().order_by('title')
    return render(request, 'professionals/job_list.html', {'jobs': jobs})


def professionals_by_job(request, job_code):
    job = Job.objects.get(code=job_code)
    if job.code == 'stylist':
        professionals = StylistProfile.objects.filter(user__job=job)
    elif job.code == 'doctor':
        professionals = DoctorProfile.objects.filter(user__job=job)
    elif job.code == 'coach':
        professionals = DoctorProfile.objects.filter(user__job=job)
    elif job.code == 'electrician':
        professionals = DoctorProfile.objects.filter(user__job=job)
    if request.user.is_authenticated:
        professionals = professionals.exclude(user=request.user)

    return render(request, 'professionals/professionals_by_job.html', {
        'job': job,
        'professionals': professionals
    })

@login_required
def manage_availability(request):
    user = request.user

    if user.role != 'professional' or user.job.code != 'stylist':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.stylist = request.user.stylistprofile
            availability.save()
            return redirect('professionals:manage_availability')

    else:
        form = AvailabilityForm()

    time_slots = time_slots = Availability.objects.filter(stylist=user.stylistprofile).order_by('weekday', 'start_time')

    return render(request, 'professionals/manage_availability.html', {
        'form': form,
        'time_slots': time_slots
    })
=======
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from appointments.forms import AvailabilityForm
from appointments.models import Availability
from appointments.utils import has_any_availability
from .models import DoctorProfile, Job, StylistProfile

JOB_PROFILE_MODEL = {
    'stylist': StylistProfile,
    'doctor': DoctorProfile,
}


def profile_view(request, profile_type, profile_id):
    profiles = {
        'stylist': StylistProfile,
        'doctor': DoctorProfile,
    }
    profile_model = profiles.get(profile_type)
    if not profile_model:
        raise Http404
    profile = get_object_or_404(profile_model, id=profile_id)
    return render(request, f'professionals/{profile_type}_profile.html', {'profile': profile})


def job_list(request):
    jobs = Job.objects.order_by('title')
    return render(request, 'professionals/job_list.html', {'jobs': jobs})


def professionals_by_job(request, job_code):
    job = get_object_or_404(Job, code=job_code)
    model = JOB_PROFILE_MODEL.get(job.code)
    if not model:
        messages.warning(request, 'پروفایل این شغل هنوز در سیستم فعال نشده است.')
        return render(request, 'professionals/professionals_by_job.html', {'job': job, 'professionals': []})

    qs = model.objects.select_related('user', 'user__job').filter(user__job=job)
    if request.user.is_authenticated:
        qs = qs.exclude(user=request.user)

    professionals = []
    for prof in qs:
        prof.can_book = has_any_availability(prof)
        # نکته مهم: برای ساخت URL رزرو از کد شغل استفاده می‌کنیم (stylist / doctor)
        prof.model_name = job.code
        professionals.append(prof)

    return render(request, 'professionals/professionals_by_job.html', {'job': job, 'professionals': professionals})


@login_required
def manage_availability(request):
    user = request.user
    if getattr(user, 'role', None) != 'professional' or not getattr(user, 'job', None):
        messages.error(request, 'ابتدا شغل خود را انتخاب کنید.')
        return redirect('accounts:dashboard')

    profile_model = JOB_PROFILE_MODEL.get(user.job.code)
    if not profile_model:
        messages.error(request, 'پروفایل این شغل هنوز پشتیبانی نمی‌شود.')
        return redirect('accounts:dashboard')

    profile_obj, _ = profile_model.objects.get_or_create(user=user)
    ctype = ContentType.objects.get_for_model(profile_model)

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            av = form.save(commit=False)
            av.professional_content_type = ctype
            av.professional_object_id = profile_obj.pk
            try:
                av.full_clean()
                av.save()
                messages.success(request, 'بازه‌ی دسترسی اضافه شد.')
            except Exception as e:
                messages.error(request, f'ثبت بازه ناموفق بود: {e}')
            return redirect('professionals:manage_availability')
    else:
        form = AvailabilityForm()

    time_slots = Availability.objects.filter(
        professional_content_type=ctype,
        professional_object_id=profile_obj.pk,
    ).order_by('specific_date', 'weekday', 'start_time')

    return render(request, 'professionals/manage_availability.html', {'form': form, 'time_slots': time_slots})
>>>>>>> 100bba5 (Inititial commit)
