<<<<<<< HEAD
from django.urls import path
from .views import register_view, login_view, logout_view, user_dashboard


app_name = 'accounts'
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', user_dashboard, name='dashboard'),
]
=======
from django.urls import path
from .views import register_view, login_view, logout_view, user_dashboard


app_name = 'accounts'
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', user_dashboard, name='dashboard'),
]
>>>>>>> 100bba5 (Inititial commit)
