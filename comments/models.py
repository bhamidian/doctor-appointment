from django.db import models
from reservation.models import Reservation


class Comment(models.Model):
    score = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    text = models.TextField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
