from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not firstname:
            raise ValueError('Users must have a first name')
        if not lastname:
            raise ValueError('Users must have a last name')

        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, phone_number, password):
        user = self.create_user(
            email,
            password=password,
            firstname=firstname,
            lastname=lastname,
            phone_number=phone_number,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'Patient {self.patient_id}'


class Specialty(models.Model):
    specialty = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.specialty


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    visit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    clinic_address = models.CharField(max_length=255)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)

    def __str__(self):
        return f'Doctor {self.doctor_id} - {self.specialty}'


class Account(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
