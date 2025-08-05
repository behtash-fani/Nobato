from django.urls import path
from .views import list_professionals_by_job
from .views import book_appointment


app_name = 'booking'

urlpatterns = [
    path('book/', book_appointment, name='book_appointment'),
    path('jobs/<slug:job_code>/', list_professionals_by_job, name='list_professionals_by_job'),
]
