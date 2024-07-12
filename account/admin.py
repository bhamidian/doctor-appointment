from django.contrib import admin
from .models import Patient, Specialty, Doctor, Account
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('email', 'firstname', 'lastname', 'is_superuser')
    search_fields = ('email', 'firstname', 'lastname')
    readonly_fields = ('user_id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'firstname', 'lastname', 'phone_number', 'password1', 'password2'),
        }),
    )

    ordering = ('email',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'balance')
    search_fields = ('patient_id',)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('specialty',)
    search_fields = ('specialty',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'specialty', 'visit_cost', 'clinic_address')
    search_fields = ('doctor_id', 'specialty__specialty')
    list_filter = ('specialty',)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstname', 'lastname', 'phone_number', 'is_superuser', 'is_staff', 'doctor', 'patient')
    search_fields = ('email', 'firstname', 'lastname', 'phone_number')
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ('firstname', 'lastname', 'phone_number')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff')
        }),
        ('Associations', {
            'fields': ('doctor', 'patient')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'firstname', 'lastname', 'phone_number', 'password1', 'password2', 'is_superuser', 'is_staff',
            'doctor', 'patient'),
        }),
    )
    ordering = ('email',)
    filter_horizontal = ()
