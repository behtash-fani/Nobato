from django.shortcuts import render, get_object_or_404
from professionals.models import Job, StylistProfile
from .forms import BookingForm
from appointments.forms import AvailabilityForm
from django.contrib.auth.decorators import login_required

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


def list_professionals_by_job(request, job_code):
    job = get_object_or_404(Job, code=job_code)
    professionals = StylistProfile.objects.select_related('user').filter(user__job=job)

    if request.user.is_authenticated:
        professionals = professionals.exclude(user=request.user)

    return render(request, 'booking/professionals_by_job.html', {
        'job': job,
        'professionals': professionals
    })
