<<<<<<< HEAD
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
=======
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import CustomUser
from professionals.models import StylistProfile, DoctorProfile

class StylistProfileInline(admin.StackedInline):
    model = StylistProfile
    fk_name = 'user'
    can_delete = False
    extra = 0
    verbose_name_plural = 'پروفایل استایلیست'

class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    fk_name = 'user'
    can_delete = False
    extra = 0
    verbose_name_plural = 'پروفایل پزشک'

INLINE_MAP = {
    'stylist': StylistProfileInline,
    'doctor': DoctorProfileInline,
}

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'role', 'job', 'is_staff']
    list_filter  = ['role', 'job', 'is_staff']
    search_fields = ['username', 'phone_number']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone_number', 'job')}),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj or obj.role != 'professional' or not obj.job:
            return []
        inline_cls = INLINE_MAP.get(obj.job.code)
        if not inline_cls:
            return []
        return [inline_cls(self.model, self.admin_site)]

    def response_add(self, request, obj, post_url_continue=None):
        url = reverse('admin:accounts_customuser_change', args=[obj.pk])
        return HttpResponseRedirect(url)

admin.site.register(CustomUser, CustomUserAdmin)
>>>>>>> 100bba5 (Inititial commit)
