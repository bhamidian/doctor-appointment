from django.test import TestCase
from .models import Account, Patient, Doctor, Specialty
from django.test import TestCase, Client
from django.urls import reverse
from .forms import PatientRegistrationForm, LoginForm


class AccountModelTest(TestCase):
    def setUp(self):
        self.specialty = Specialty.objects.create(specialty='Cardiology')
        self.doctor = Doctor.objects.create(visit_cost=100, clinic_address='123 Street', specialty=self.specialty)
        self.patient = Patient.objects.create()

    def test_create_account(self):
        account = Account.objects.create_user(
            email='test@example.com',
            firstname='John',
            lastname='Doe',
            phone_number='1234567890',
            password='testpassword',
        )
        self.assertEqual(account.email, 'test@example.com')
        self.assertEqual(account.firstname, 'John')
        self.assertEqual(account.lastname, 'Doe')
        self.assertTrue(account.check_password('testpassword'))

    def test_create_superuser(self):
        superuser = Account.objects.create_superuser(
            email='admin@example.com',
            firstname='Admin',
            lastname='User',
            phone_number='1234567890',
            password='adminpassword',
        )
        self.assertTrue(superuser.is_superuser)

    def test_patient_model(self):
        self.assertEqual(self.patient.balance, 0.0)

    def test_doctor_model(self):
        self.assertEqual(self.doctor.visit_cost, 100)
        self.assertEqual(self.doctor.clinic_address, '123 Street')
        self.assertEqual(self.doctor.specialty.specialty, 'Cardiology')

    def test_specialty_model(self):
        self.assertEqual(self.specialty.specialty, 'Cardiology')


class AccountViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient = Patient.objects.create()
        self.user = Account.objects.create_user(
            email='user@example.com',
            firstname='John',
            lastname='Doe',
            phone_number='1234567890',
            password='testpassword',
            # patient=self.patient,
        )

    def test_register_view(self):
        response = self.client.get(reverse('register_patient'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], PatientRegistrationForm)

        response = self.client.post(reverse('register_patient'), {
            'email': 'newuser@example.com',
            'firstname': 'New',
            'lastname': 'User',
            'phone_number': '0987654321',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

        response = self.client.post(reverse('login'), {
            'username': 'user@example.com',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_profile_view(self):
        self.client.login(email='user@example.com', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertIn('reservation', response.context)
        self.assertIn('comments', response.context)

        response = self.client.post(reverse('profile'), {
            'firstname': 'Updated',
            'lastname': 'Name',
            'phone_number': '1122334455',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.firstname, 'Updated')
        self.assertEqual(self.user.lastname, 'Name')
        self.assertEqual(self.user.phone_number, '1122334455')
