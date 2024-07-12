from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account, Patient


class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=255)
    lastname = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = Account
        fields = ('email', 'firstname', 'lastname', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.firstname = self.cleaned_data['firstname']
        user.lastname = self.cleaned_data['lastname']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            patient = Patient.objects.create()
            user.patient = patient
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)
