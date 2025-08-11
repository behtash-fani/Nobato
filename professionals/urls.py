from django.urls import path
from .views import job_list, professionals_by_job, manage_availability, profile_view


app_name = 'professionals'
urlpatterns = [
    path('jobs/', job_list, name='job_list'),
    path('<slug:job_code>/', professionals_by_job, name='professionals_by_job'),
    path('availability/', manage_availability, name='manage_availability'),
    path('<str:profile_type>/<int:profile_id>/', profile_view, name='profile_detail'),
]
