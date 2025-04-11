from django.test import TestCase
from django.utils import timezone
from django.core import mail
from decimal import Decimal
from django.core.exceptions import ValidationError
from .models import Reservation, EmailLog
from .tasks import send_reservation_email
from datetime import timedelta
from custom_auth.models import CustomUser as User
from accommodations.models import Accommodation
from unittest import mock

class ReservationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.accommodation = Accommodation.objects.create(
            name="Test Lodge",
            price_per_night=Decimal('100.00')
        )
        
        check_in = timezone.now() + timedelta(days=1)
        check_out = timezone.now() + timedelta(days=3)
        
        self.reservation = Reservation.objects.create(
            user=self.user,
            check_in_date=check_in,
            check_out_date=check_out,
            status='confirmed',
            number_of_guests=2,
            accommodation=self.accommodation
        )

    def test_price_calculation(self):
        check_in = timezone.now() + timedelta(days=1)
        check_out = timezone.now() + timedelta(days=4)
        
        reservation = Reservation.objects.create(
            user=self.user,
            check_in_date=check_in,
            check_out_date=check_out,
            number_of_guests=2,
            status='confirmed',
            accommodation=self.accommodation
        )
        
        expected_price = Decimal('360.0000')  # 3 nuits * 100 + 20% taxes
        self.assertEqual(reservation.total_price, expected_price)

    def test_reservation_capacity_limit(self):
        # Créer une première réservation
        existing_reservation = Reservation.objects.create(
            user=self.user,
            check_in_date=timezone.now() + timedelta(days=5),
            check_out_date=timezone.now() + timedelta(days=7),
            number_of_guests=2,
            status='confirmed',
            accommodation=self.accommodation
        )
        
      # Tenter de créer une réservation qui chevauche
        conflicting_reservation = Reservation(
            user=self.user,
            check_in_date=timezone.now() + timedelta(days=6),
            check_out_date=timezone.now() + timedelta(days=8),
            number_of_guests=2,
            status='confirmed',
            accommodation=self.accommodation
        )
        
        with self.assertRaises(ValidationError):
            conflicting_reservation.full_clean()

class EmailNotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.accommodation = Accommodation.objects.create(
            name="Test Lodge",
            price_per_night=Decimal('100.00')
        )
        
        check_in = timezone.now() + timedelta(days=1)
        check_out = timezone.now() + timedelta(days=3)
        
        self.reservation = Reservation.objects.create(
            user=self.user,
            check_in_date=check_in,
            check_out_date=check_out,
            status='confirmed',
            number_of_guests=2,
            accommodation=self.accommodation
        )

    @mock.patch('reservations.tasks.render_to_string')
    def test_send_confirmation_email(self, mock_render):
        # Mock le rendu du template
        mock_render.return_value = "Email content"
        
        result = send_reservation_email.delay(self.reservation.id, 'confirmation')
        
        # Vérifier que le template a reçu les bonnes variables
        context = mock_render.call_args[0][1]
        self.assertEqual(context['service'], self.accommodation.name)
        
        # Verify email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Confirmation', mail.outbox[0].subject)
        
        # Verify email log was created
        email_log = EmailLog.objects.filter(
            reservation=self.reservation,
            email_type='confirmation'
        ).first()
        self.assertIsNotNone(email_log)
        self.assertEqual(email_log.status, 'sent')

    def test_send_reminder_email(self):
        result = send_reservation_email.delay(self.reservation.id, 'reminder')
        self.assertTrue(result.successful())
        
        # Verify email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Rappel', mail.outbox[0].subject)

    def test_pdf_generation(self):
        result = send_reservation_email.delay(self.reservation.id, 'confirmation')
        self.assertTrue(result.successful())
        
        # Check if PDF is attached
        email = mail.outbox[0]
        self.assertEqual(len(email.attachments), 1)
        self.assertTrue(email.attachments[0][0].endswith('.pdf'))

    def test_failed_email_sending(self):
        # Test with invalid email
        self.user.email = "invalid@nonexistent.domain"
        self.user.save()
        
        result = send_reservation_email.delay(self.reservation.id, 'confirmation')
        
        email_log = EmailLog.objects.filter(
            reservation=self.reservation,
            email_type='confirmation'
        ).first()
        self.assertEqual(email_log.status, 'failed')

    def test_email_content(self):
        result = send_reservation_email.delay(self.reservation.id, 'confirmation')
        email = mail.outbox[0]
        
        # Verify email content
        self.assertIn(self.user.first_name, email.body)
        self.assertIn(str(self.reservation.id), email.body)
        self.assertIn(str(self.reservation.check_in_date), email.body)