from django.db import models
from account.models import Patient, Account


class VisitTime(models.Model):
    WEEK_DAYS = [
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    ]

    doctor = models.ForeignKey(Account, on_delete=models.CASCADE)
    week_day = models.IntegerField(choices=WEEK_DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} - {self.get_week_day_display()} ({self.start_time} - {self.end_time})"


class Reservation(models.Model):
    patient = models.ForeignKey(Account, on_delete=models.CASCADE)
    visit = models.ForeignKey(VisitTime, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation: {self.patient} for {self.visit}"


class Transaction(models.Model):
    from_wallet = models.ForeignKey(Account, related_name='transactions_from', on_delete=models.CASCADE)
    to_wallet = models.ForeignKey(Account, related_name='transactions_to', on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    def __str__(self):
        return f"Transaction from {self.from_wallet} to {self.to_wallet} for reservation {self.reservation}"
