from django.shortcuts import render
from account.models import Account, Specialty


def index(request):
    doctors = Account.objects.filter(doctor__isnull=False).all()

    if request.method == "POST":
        specialty = Specialty.objects.get(pk=request.POST['specialty'])
        doctors = Account.objects.filter(doctor__specialty=specialty).all()

    specialties = Specialty.objects.all()
    return render(request, 'home.html', {'doctors': doctors, 'specialties': specialties})
