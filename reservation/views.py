from django.shortcuts import render, get_object_or_404, redirect
from account.models import Doctor, Account
from .models import VisitTime, Reservation, Transaction


def reservation_get(request, doctor_id: int):
    doctor = Account.objects.get(pk=doctor_id)
    if doctor.doctor is None:
        return redirect('home')

    times = VisitTime.objects.filter(doctor=doctor).filter(is_reserved=False).all()

    return render(request, 'reserve.html', {'doctor': doctor, 'times': times})


def reservation_post(request):
    if not request.method == 'POST':
        return redirect('home')

    doctor_id = request.POST.get('doctor_id')
    doctor = Account.objects.get(pk=doctor_id)
    if doctor.doctor is None:
        return redirect('home')

    times = VisitTime.objects.filter(doctor=doctor).filter(is_reserved=False).all()

    if not request.user.is_authenticated:
        return redirect('login')

    time_id = request.POST.get('time')
    time = get_object_or_404(VisitTime, pk=time_id)
    user = get_object_or_404(Account, user_id=request.user.user_id)
    print(user.patient)

    if user.patient.balance < doctor.doctor.visit_cost:
        # TODO add balance error message
        return render(request, 'reserve.html', {'doctor': doctor, 'times': times})

    user.patient.balance -= doctor.doctor.visit_cost
    user.save()

    time.is_reserved = True
    time.save()

    reserver_obj = Reservation.objects.create(doctor=doctor, visit=time)
    Transaction.objects.create(from_wallet=user, to_wallet=doctor, reservation=reserver_obj)

    return redirect('profile')
