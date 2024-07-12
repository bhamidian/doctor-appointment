from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_patient, name='register_patient'),
    path('login/', views.login_view, name='login'),
    path('', views.profile_view, name='profile'),
]
