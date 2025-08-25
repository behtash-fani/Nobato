<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm

from professionals.models import Job

def home_view(request):
    jobs = Job.objects.order_by('title')
    return render(request, 'home.html', {'jobs': jobs})



def register_view(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')  # بعداً صفحه داشبورد هر نقش
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:dashboard')  # بعداً مسیر پنل
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def user_dashboard(request):
    user = request.user

    if user.role == 'professional':
        if user.job and user.job.code == 'stylist':
            if not hasattr(user, 'stylistprofile'):
                return redirect('professionals:edit_stylist_profile')

            profile = user.stylistprofile
            return render(
                request,
                'professionals/stylist_dashboard.html',
                {'user': user, 'profile': profile}
            )

    elif user.role == 'customer':
        return render(request, 'accounts/customer_dashboard.html', {'user': user})

    return redirect('home')



=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.forms import modelform_factory
from django import forms
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from .forms import JobSelectForm, CustomLoginForm, CustomUserCreationForm
from .models import CustomUser
from professionals.models import Job, StylistProfile, DoctorProfile
from appointments.models import Availability
from appointments.forms import AvailabilityForm


def home_view(request):
    jobs = Job.objects.order_by('title')
    return render(request, 'home.html', {'jobs': jobs})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# مپ شغل ← مدل پروفایل
JOB_PROFILE_MODEL = {
    'stylist': StylistProfile,
    'doctor': DoctorProfile,
}


# هلسپر ریدایرکت با تب فعال
def redirect_with_tab(tab_name: str):
    url = reverse('accounts:dashboard')
    return redirect(f"{url}?{tab_name}")


@login_required
def user_dashboard(request):
    user: CustomUser = request.user

    # تب فعال برای رندر GET (پیش‌فرض overview)
    active_tab = request.GET.get('tab', 'overview')

    job_form = JobSelectForm(instance=user)

    profile_model = None
    profile_obj = None
    profile_form = None
    availability_qs = None
    availability_form = None

    # اگر کاربر شغل دارد، فرم پروفایل و دسترسی‌ها را آماده کن
    if user.job and user.job.code in JOB_PROFILE_MODEL:
        profile_model = JOB_PROFILE_MODEL[user.job.code]
        profile_obj, _ = profile_model.objects.get_or_create(user=user)

        # فرم داینامیک پروفایل با ویجت‌های بوت‌استرپ
        DynamicProfileForm = modelform_factory(
            profile_model,
            fields='__all__',
            widgets={
                'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                'salon_name': forms.TextInput(attrs={'class': 'form-control'}),
                'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
                'specialty_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                'clinic_name': forms.TextInput(attrs={'class': 'form-control'}),
                'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            }
        )
        profile_form = DynamicProfileForm(instance=profile_obj)
        if 'user' in profile_form.fields:
            profile_form.fields.pop('user')

        # لیست دسترسی‌ها + فرمش
        ctype = ContentType.objects.get_for_model(profile_model)
        availability_qs = Availability.objects.filter(
            professional_content_type=ctype,
            professional_object_id=profile_obj.pk
        ).order_by('specific_date', 'weekday', 'start_time')
        availability_form = AvailabilityForm()

    # هندل POST
    if request.method == 'POST':
        form_name = request.POST.get('form_name')

        # 1) ذخیره شغل
        if form_name == 'job':
            job_form = JobSelectForm(request.POST, instance=user)
            if job_form.is_valid():
                job_form.save()
                if user.role != 'professional':
                    user.role = 'professional'
                    user.save(update_fields=['role'])
                messages.success(request, 'شغل شما ذخیره شد.')
                # بعد از انتخاب شغل کاربر را به تب پروفایل بفرست
                return redirect_with_tab('profile')
            else:
                messages.error(request, 'ذخیره شغل ناموفق بود. ورودی‌ها را بررسی کنید.')
                active_tab = 'overview'  # در همان تب بماند

        # 2) ذخیره پروفایل تخصصی
        elif form_name == 'profile' and (user.job and user.job.code in JOB_PROFILE_MODEL):
            profile_model = JOB_PROFILE_MODEL[user.job.code]
            profile_obj, _ = profile_model.objects.get_or_create(user=user)
            DynamicProfileForm = modelform_factory(profile_model, fields='__all__')
            profile_form = DynamicProfileForm(request.POST, request.FILES, instance=profile_obj)
            if 'user' in profile_form.fields:
                profile_form.fields.pop('user')

            if profile_form.is_valid():
                obj = profile_form.save(commit=False)
                obj.user = user
                obj.save()
                messages.success(request, 'پروفایل شما ذخیره شد.')
                return redirect_with_tab('profile')
            else:
                messages.error(request, 'ذخیره پروفایل ناموفق بود.')
                active_tab = 'profile'  # خطاها را در همان تب نشان بده

        # 3) افزودن زمان آزاد
        elif form_name == 'availability_add' and (user.job and user.job.code in JOB_PROFILE_MODEL):
            profile_model = JOB_PROFILE_MODEL[user.job.code]
            profile_obj, _ = profile_model.objects.get_or_create(user=user)
            ctype = ContentType.objects.get_for_model(profile_model)

            availability_form = AvailabilityForm(request.POST)
            if availability_form.is_valid():
                av = availability_form.save(commit=False)
                av.professional_content_type = ctype
                av.professional_object_id = profile_obj.pk
                try:
                    av.full_clean()  # اجرای clean() مدل (تداخل/بازه معکوس)
                    av.save()
                    messages.success(request, 'بازه‌ی دسترسی اضافه شد.')
                    return redirect_with_tab('availability')
                except ValidationError as e:
                    # خطاهای ولیدیشن مدل
                    for field, errs in e.message_dict.items():
                        for err in errs:
                            if field in availability_form.fields:
                                availability_form.add_error(field, err)
                            else:
                                availability_form.add_error(None, err)
                    messages.error(request, 'ثبت بازه ناموفق بود.')
            else:
                messages.error(request, 'ورودی‌های بازه را بررسی کنید.')
            active_tab = 'availability'

            # رفرش لیست بازه‌ها برای نمایش مجدد فرم با خطا
            availability_qs = Availability.objects.filter(
                professional_content_type=ctype,
                professional_object_id=profile_obj.pk
            ).order_by('weekday', 'start_time')

        # 4) حذف زمان آزاد
        elif form_name == 'availability_delete' and (user.job and user.job.code in JOB_PROFILE_MODEL):
            av_id = request.POST.get('availability_id')
            if av_id:
                profile_model = JOB_PROFILE_MODEL[user.job.code]
                profile_obj, _ = profile_model.objects.get_or_create(user=user)
                ctype = ContentType.objects.get_for_model(profile_model)
                Availability.objects.filter(
                    id=av_id,
                    professional_content_type=ctype,
                    professional_object_id=profile_obj.pk
                ).delete()
                messages.success(request, 'بازه حذف شد.')
                return redirect_with_tab('availability')
            active_tab = 'availability'

    ctx = {
        'job_form': job_form,
        'profile_form': profile_form,
        'profile_model_name': profile_model.__name__ if profile_model else None,
        'user': user,
        'availability_form': availability_form,
        'availability_list': availability_qs,
        'active_tab': active_tab,  # ← خیلی مهم
    }
    return render(request, 'accounts/dashboard.html', ctx)
>>>>>>> 100bba5 (Inititial commit)
