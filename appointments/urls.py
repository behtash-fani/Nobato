<<<<<<< HEAD
from django.urls import path
from .views import delete_availability, edit_availability, book_appointment


app_name = 'appointments'
urlpatterns = [
    path('availability/edit/<int:slot_id>/', edit_availability, name='edit_availability'),
    path('availability/delete/<int:pk>/', delete_availability, name='delete_availability'),
    path('book/', book_appointment, name='book_appointment'),
]



=======
from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('<str:profile_type>/<int:profile_id>/book/', views.book_start, name='book_start'),
    path('<str:profile_type>/<int:profile_id>/book/<date_str>/', views.book_times, name='book_times'),
]
>>>>>>> 100bba5 (Inititial commit)
