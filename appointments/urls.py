from django.urls import path
from .views import delete_availability, edit_availability, book_appointment


app_name = 'appointments'
urlpatterns = [
    path('availability/edit/<int:slot_id>/', edit_availability, name='edit_availability'),
    path('availability/delete/<int:pk>/', delete_availability, name='delete_availability'),
    path('book/', book_appointment, name='book_appointment'),
]



