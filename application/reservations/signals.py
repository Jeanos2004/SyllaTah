from django.core.mail import EmailMessage
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework import status
from io import BytesIO
import logging
from xhtml2pdf import pisa
from .models import Reservation, EmailLog

logger = logging.getLogger(__name__)

def generate_pdf(instance):
    """Separate PDF generation for better error handling"""
    try:
        context = {
            'reservation': instance,
            'user_name': instance.user.get_full_name(),
            'service_type': instance.service_type,
            'check_in_date': instance.check_in_date,
            'check_out_date': instance.check_out_date,
            'reservation_date': instance.reservation_date,
            'total_price': instance.total_price,
            'reservation_id': instance.id,
        }
        template = get_template('reservations/reservation_pdf.html')
        html = template.render(context)
        pdf_buffer = BytesIO()
        pdf_status = pisa.CreatePDF(html, dest=pdf_buffer)
        
        if pdf_status.err:
            logger.error(f'PDF Generation Error for reservation {instance.id}')
            return None
        return pdf_buffer
    except Exception as e:
        logger.error(f'PDF Generation Exception: {str(e)}')
        return None

@receiver(pre_save, sender=Reservation)
def validate_reservation(sender, instance, **kwargs):
    """Validate reservation data before saving"""
    if instance.check_in_date >= instance.check_out_date:
        raise ValidationError({
            'check_in_date': 'Check-in date must be before check-out date',
            'status': status.HTTP_400_BAD_REQUEST
        })

class EmailService:
    @staticmethod
    def send_confirmation(instance, pdf_buffer):
        try:
            email = EmailMessage(
                subject=f'SyllaTah - Confirmation de réservation #{instance.id}',
                body=EmailService._get_email_body(instance),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[instance.user.email],
            )
            
            if pdf_buffer:
                email.attach(
                    f'recu_reservation_{instance.id}.pdf',
                    pdf_buffer.getvalue(),
                    'application/pdf'
                )
            
            email.send()
            EmailLog.objects.create(
                reservation=instance,
                email_type='confirmation',
                status='sent',
                recipient=instance.user.email
            )
            return True
        except Exception as e:
            logger.error(f'Email sending failed: {str(e)}')
            EmailLog.objects.create(
                reservation=instance,
                email_type='confirmation',
                status='failed',
                recipient=instance.user.email,
                error_message=str(e)
            )
            return False

    @staticmethod
    def _get_email_body(instance):
        return f"""
        Bonjour {instance.user.first_name},

        Nous vous remercions d'avoir choisi SyllaTah pour votre réservation.

        Détails de votre réservation :
        - Numéro : {instance.id}
        - Type de service : {instance.service_type}
        - Date d'arrivée : {instance.check_in_date}
        - Date de départ : {instance.check_out_date}
        - Date de réservation : {instance.reservation_date}
        - Montant total : {instance.total_price} €

        Vous trouverez ci-joint votre reçu de réservation.

        Pour visualiser ou télécharger votre reçu ultérieurement, connectez-vous à votre compte SyllaTah.

        Cordialement,
        L'équipe SyllaTah
        """

@receiver(post_save, sender=Reservation)
def reservation_confirmation(sender, instance, created, **kwargs):
    if created:
        pdf_buffer = generate_pdf(instance)
        EmailService.send_confirmation(instance, pdf_buffer)