from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Availability
from .forms import AvailabilityForm
from django.shortcuts import get_object_or_404


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
