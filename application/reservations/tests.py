from django.test import TestCase

from django.contrib.auth.models import User
from django.utils import timezone
from .models import Reservation
from .tasks import send_reservation_email
from datetime import timedelta

class NotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.reservation = Reservation.objects.create(
            user=self.user,
            check_in_date=timezone.now().date() + timedelta(days=1),
            check_out_date=timezone.now().date() + timedelta(days=3),
            status='confirmed'
        )

    def test_send_confirmation_email(self):
        result = send_reservation_email.delay(self.reservation.id, 'confirmation')
        self.assertTrue(result.successful())

    def test_send_reminder_email(self):
        result = send_reservation_email.delay(self.reservation.id, 'reminder')
        self.assertTrue(result.successful())