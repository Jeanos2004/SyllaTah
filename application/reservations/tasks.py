from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
from .models import Reservation, EmailLog

@shared_task(bind=True, max_retries=3)
def send_reservation_email(self, reservation_id, email_type):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        
        templates = {
            'confirmation': 'emails/reservation_confirmation.html',
            'reminder': 'emails/reservation_reminder.html',
            'cancellation': 'emails/reservation_cancellation.html',
            'payment': 'emails/payment_confirmation.html'
        }
        
        subjects = {
            'confirmation': 'SyllaTah - Confirmation de votre réservation',
            'reminder': 'SyllaTah - Rappel de votre réservation à venir',
            'cancellation': 'SyllaTah - Annulation de votre réservation',
            'payment': 'SyllaTah - Confirmation de paiement'
        }

        context = {
            'reservation': reservation,
            'user': reservation.user,
            'service': reservation.service_type,
            'total_price': reservation.total_price,
            'site_url': 'http://localhost:3000'  # À adapter selon votre environnement
        }

        html_content = render_to_string(templates[email_type], context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subjects[email_type],
            body=text_content,
            from_email='jeankelouaouamouno71@gmail.com',
            to=[reservation.user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        EmailLog.objects.create(
            reservation=reservation,
            email_type=email_type,
            status='sent',
            recipient=reservation.user.email
        )

    except Exception as e:
        EmailLog.objects.create(
            reservation_id=reservation_id,
            email_type=email_type,
            status='failed',
            recipient=reservation.user.email if reservation else 'unknown',
            error_message=str(e)
        )
        raise self.retry(exc=e, countdown=300)  # Retry after 5 minutes

@shared_task
def send_reminder_notifications():
    """Envoie des rappels pour les réservations à venir"""
    tomorrow = timezone.now().date() + timedelta(days=1)
    upcoming = Reservation.objects.filter(
        check_in_date=tomorrow,
        status='confirmed'
    )
    
    for reservation in upcoming:
        send_reservation_email.delay(reservation.id, 'reminder')