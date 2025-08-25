<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Availability
from .forms import AvailabilityForm
from django.shortcuts import get_object_or_404
from professionals.models import Job, StylistProfile
from .forms import BookingForm

@login_required
def edit_availability(request, slot_id):
    user = request.user
    profile = user.stylistprofile

    slot = get_object_or_404(Availability, id=slot_id, stylist=profile)

    if request.method == 'POST':
        form = AvailabilityForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            return redirect('appointments:manage_availability')
    else:
        form = AvailabilityForm(instance=slot)

    return render(request, 'appointments/edit_availability.html', {'form': form})


@login_required
def delete_availability(request, pk):
    user = request.user
    slot = get_object_or_404(Availability, pk=pk, stylist=user)
    slot.delete()
    return redirect('appointments:manage_availability')




@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = request.user
            appointment.save()
            return redirect('appointments:appointment_success')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form})
=======
from datetime import date, datetime, timedelta
from typing import List, Set

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from professionals.models import DoctorProfile, StylistProfile
from .models import Availability, Booking
from .utils import free_slots_for_date, has_any_availability


PROFILE_MAP = {
    'stylist': StylistProfile,
    'doctor': DoctorProfile,
}


def _resolve_profile(profile_type: str, profile_id: int):
    model = PROFILE_MAP.get(profile_type)
    if not model:
        raise Http404
    return get_object_or_404(model, pk=profile_id)


def _parse_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HttpResponseBadRequest("invalid date")


@login_required
def book_start(request, profile_type: str, profile_id: int):
    profile = _resolve_profile(profile_type, profile_id)

    if not has_any_availability(profile):
        messages.warning(request, "زمان آزاد برای این متخصص ثبت نشده است.")
        return redirect('professionals:professionals_by_job', job_code=profile.user.job.code)

    today = date.today()
    horizon = today + timedelta(days=14)

    ctype = ContentType.objects.get_for_model(profile.__class__)
    av_qs = Availability.objects.filter(
        professional_content_type=ctype,
        professional_object_id=profile.pk
    )

    specific_dates = av_qs.filter(specific_date__gte=today, specific_date__lte=horizon).values_list('specific_date', flat=True).distinct()

    dates_with_free: List[date] = []

    if specific_dates:
        uniq: Set[date] = set()
        for d in specific_dates:
            d = d  # DateField
            free = free_slots_for_date(profile, d, step_minutes=30)
            if free:
                uniq.add(d)
        dates_with_free = sorted(uniq)
    else:
        # برای weekly فقط نزدیک‌ترین رخداد هر روز هفته را نشان بده
        seen_wd: Set[int] = set()
        for i in range(0, 15):
            d = today + timedelta(days=i)
            wd = d.weekday()
            avail_wd = (wd + 1) % 7
            if avail_wd in seen_wd:
                continue
            has_av_for_wd = av_qs.filter(specific_date__isnull=True, weekday=avail_wd).exists()
            if not has_av_for_wd:
                continue
            free = free_slots_for_date(profile, d, step_minutes=30)
            if free:
                dates_with_free.append(d)
                seen_wd.add(avail_wd)

    ctx = {
        'profile': profile,
        'profile_type': profile_type,
        'dates_with_free': dates_with_free,
    }
    return render(request, 'appointments/book_start.html', ctx)


@login_required
def book_times(request, profile_type: str, profile_id: int, date_str: str):
    profile = _resolve_profile(profile_type, profile_id)
    day = _parse_date(date_str)

    free = free_slots_for_date(profile, day, step_minutes=30)
    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')
        if not start or not end:
            return HttpResponseBadRequest("missing time")

        try:
            s = datetime.strptime(start, "%H:%M").time()
            e = datetime.strptime(end, "%H:%M").time()
        except ValueError:
            return HttpResponseBadRequest("invalid time")

        if (s, e) not in free:
            messages.error(request, "این بازه دیگر در دسترس نیست.")
            return redirect('appointments:book_times', profile_type=profile_type, profile_id=profile_id, date_str=date_str)

        ctype = ContentType.objects.get_for_model(profile.__class__)
        booking = Booking(
            customer=request.user,
            professional_content_type=ctype,
            professional_object_id=profile.pk,
            date=day,
            start_time=s,
            end_time=e,
            status=Booking.STATUS_CONFIRMED,
        )
        try:
            booking.full_clean()
            booking.save()
            messages.success(request, "رزرو با موفقیت ثبت شد.")
            return redirect('professionals:professionals_by_job', job_code=profile.user.job.code)
        except Exception as ex:
            messages.error(request, str(ex))

    ctx = {
        'profile': profile,
        'profile_type': profile_type,
        'day': day,
        'free_slots': free,
    }
    return render(request, 'appointments/book_times.html', ctx)
>>>>>>> 100bba5 (Inititial commit)
