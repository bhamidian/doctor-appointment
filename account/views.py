from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import PatientRegistrationForm, LoginForm
from reservation.models import Reservation
from comments.models import Comment


def register_patient(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='/accounts/login/')
def profile_view(request):
    # TODO select * comment and reservations
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        phone_number = request.POST['phone_number']

        user = request.user
        user.firstname = first_name
        user.lastname = last_name
        user.phone_number = phone_number
        user.save()
        return redirect('profile')

    reservations = Reservation.objects.filter(patient=request.user).all()
    comments = Comment.objects.filter(reservation__in=reservations).all()
    return render(request, 'profile.html', {"reservation": reservations, "comments": comments})
