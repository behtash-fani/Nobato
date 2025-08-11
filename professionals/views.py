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
