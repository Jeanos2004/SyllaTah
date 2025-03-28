from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Reservation, EmailLog

def send_reservation_email(reservation_id, email_type):
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
            'site_url': 'http://localhost:3000'
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
        return True

    except Exception as e:
        EmailLog.objects.create(
            reservation_id=reservation_id,
            email_type=email_type,
            status='failed',
            recipient=reservation.user.email if 'reservation' in locals() else 'unknown',
            error_message=str(e)
        )
        return False