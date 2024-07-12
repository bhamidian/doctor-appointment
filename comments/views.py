from django.shortcuts import render
from .models import Comment
from reservation.models import Reservation


def comment(request, id: int):
    return render(request, 'comment.html', {'id': id})


def add_comment(request):
    if not request.method == 'POST':
        return render(request, 'comment.html')

    title = request.POST.get('title')
    text = request.POST.get('text')
    score = request.POST.get('score')
    reserve_id = request.POST.get('reserve_id')
    reserve = Reservation.objects.get(id=reserve_id)

    Comment.objects.create(title=title, text=text, score=score, reserve=reserve)
    return render(request, 'comment.html')
