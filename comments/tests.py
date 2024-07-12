from django.utils import timezone
from django.contrib.auth import get_user_model
from account.models import Patient, Account, Doctor, Specialty
from reservation.models import VisitTime, Reservation, Transaction
from django.test import TestCase, Client
from .models import Comment
from django.urls import reverse

User = get_user_model()


class CommentViewTests(TestCase):
    def setUp(self):
        self.client = Client()

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
        self.comment = Comment.objects.create(
            score=5,
            title='Great Service',
            text='The service was excellent!',
            reservation=self.reservation,
        )

    def test_comment_view(self):
        response = self.client.get(reverse('comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comment.html')
        self.assertEqual(response.context['id'], self.comment.id)

    def test_add_comment_view_get(self):
        response = self.client.get(reverse('add_comment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comment.html')

