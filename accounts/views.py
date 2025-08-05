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



