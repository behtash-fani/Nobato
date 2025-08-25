<<<<<<< HEAD
from django.contrib import admin

# Register your models here.
=======
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from .models import Availability, Booking


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'professional_str', 'specific_date', 'weekday', 'start_time', 'end_time')
    list_filter = ('specific_date', 'weekday')
    search_fields = ('professional_object_id',)
    ordering = ('specific_date', 'weekday', 'start_time')

    def professional_str(self, obj):
        return f"{obj.professional} [{obj.professional_content_type_id}:{obj.professional_object_id}]"
    professional_str.short_description = 'Professional'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'professional_str', 'date', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('customer__username', 'customer__first_name', 'customer__last_name', 'professional_object_id')
    ordering = ('-date', 'start_time')

    def professional_str(self, obj):
        return f"{obj.professional} [{obj.professional_content_type_id}:{obj.professional_object_id}]"
    professional_str.short_description = 'Professional'
>>>>>>> 100bba5 (Inititial commit)
