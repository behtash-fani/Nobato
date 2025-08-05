from django.urls import path
from .views import job_list, professionals_by_job, edit_stylist_profile, manage_availability


app_name = 'professionals'
urlpatterns = [
    path('edit-profile/', edit_stylist_profile, name='edit_stylist_profile'),
    path('jobs/', job_list, name='job_list'),
    path('jobs/<slug:job_code>/', professionals_by_job, name='professionals_by_job'),
    path('availability/', manage_availability, name='manage_availability'),
]
