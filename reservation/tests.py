from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from account.models import Patient, Account, Doctor, Specialty
from .models import VisitTime, Reservation, Transaction

User = get_user_model()


class ReservationModelTestCase(TestCase):

    def setUp(self):
        self.specialty = Specialty.objects.create(specialty="test")
        self.doctor = Doctor.objects.create(visit_cost=50.00, clinic_address='123 Main St', specialty=self.specialty)
        self.doctor_user = Account.objects.create_user(email='doctor@example.com', firstname='John', lastname='Doe',
                                                    phone_number='123456789',
                                                       password='password123')
        self.doctor_user.doctor = self.doctor
        self.doctor_user.save()

        self.patient = Patient.objects.create(balance=200.00)
        self.patient_user = Account.objects.create_user(email='patient@example.com', firstname='Alice',
                                                        lastname='Smith',
                                                        phone_number='987654321',
                                                        password='password456')
        self.patient_user.patient = self.patient
        self.patient_user.save()

        self.visit_time = VisitTime.objects.create(doctor=self.doctor_user, week_day=0, start_time=timezone.now().time()
                                                   , end_time=(timezone.now() + timezone.timedelta(hours=1)).time())
        self.reservation = Reservation.objects.create(patient=self.patient_user, visit=self.visit_time)

    def test_visit_time_creation(self):
        self.assertIsInstance(self.visit_time, VisitTime)
        self.assertEqual(self.visit_time.doctor, self.doctor_user)
        self.assertFalse(self.visit_time.is_reserved)

    def test_reservation_creation(self):
        reservation = Reservation.objects.create(patient=self.patient_user, visit=self.visit_time)
        self.assertIsInstance(reservation, Reservation)
        self.assertEqual(reservation.patient, self.patient_user)
        self.assertEqual(reservation.visit, self.visit_time)

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(from_wallet=self.patient_user, to_wallet=self.doctor_user,
                                                 reservation=self.reservation)
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.from_wallet, self.patient_user)
        self.assertEqual(transaction.to_wallet, self.doctor_user)
        self.assertEqual(transaction.reservation, self.reservation)

