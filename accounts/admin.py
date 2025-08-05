from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from professionals.models import StylistProfile


class StylistProfileInline(admin.StackedInline):
    model = StylistProfile
    can_delete = False
    verbose_name_plural = 'پروفایل استایلیست'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'role', 'job', 'is_staff']
    list_filter = ['role', 'job', 'is_staff']
    search_fields = ['username', 'phone_number']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone_number', 'job')}),
    )

    inlines = [StylistProfileInline]


admin.site.register(CustomUser, CustomUserAdmin)
