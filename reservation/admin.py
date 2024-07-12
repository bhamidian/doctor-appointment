from django.contrib import admin
from .models import VisitTime, Reservation, Transaction


@admin.register(VisitTime)
class VisitTimeAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'week_day', 'start_time', 'end_time', 'is_reserved')
    search_fields = ('doctor__email', 'doctor__firstname', 'doctor__lastname')
    list_filter = ('week_day', 'is_reserved')
    ordering = ('doctor', 'week_day', 'start_time')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'visit')
    search_fields = ('patient__email', 'patient__firstname', 'patient__lastname', 'visit__doctor__email')
    list_filter = ('visit__week_day',)
    ordering = ('-visit__start_time',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('from_wallet', 'to_wallet', 'reservation')
    search_fields = ('from_wallet__email', 'to_wallet__email', 'reservation__patient__email')
    list_filter = ('from_wallet', 'to_wallet')
    ordering = ('-reservation',)
