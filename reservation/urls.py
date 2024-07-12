from django.urls import path
from . import views

urlpatterns = [
    path("<int:doctor_id>", views.reservation_get, name="reserve"),
    path("", views.reservation_post, name="reservation"),
]
