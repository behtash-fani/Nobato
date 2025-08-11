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
