import io
import logging
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings

logger = logging.getLogger(__name__)

class PDFService:
    @staticmethod
    def generate_reservation_pdf(reservation, context):
        try:
            template = get_template('reservations/reservation_pdf.html')
            html = template.render(context)
            pdf_file = io.BytesIO()
            
            # Ajout de la gestion de la taille maximale
            if len(html.encode('utf-8')) > settings.MAX_PDF_SIZE_BYTES:
                raise ValueError("PDF content exceeds maximum allowed size")
            
            pdf = pisa.CreatePDF(html, dest=pdf_file)
            
            if pdf.err:
                logger.error(f"Error generating PDF for reservation {reservation.id}: {pdf.err}")
                raise Exception("PDF generation failed")
            
            pdf_file.seek(0)
            return pdf_file
        except Exception as e:
            logger.error(f"PDF generation error for reservation {reservation.id}: {str(e)}")
            raise

class ReservationService:
    @staticmethod
    def prepare_email_context(reservation):
        return {
            'reservation': reservation,
            'user': reservation.user,
            'service': reservation.get_service_name(),
            'total_price': reservation.total_price,
            'site_url': settings.SITE_URL,
            'company_name': settings.COMPANY_NAME,
            'support_email': settings.SUPPORT_EMAIL,
        }

    @staticmethod
    def validate_reservation(reservation):
        if not reservation.is_valid():
            logger.error(f"Invalid reservation data for reservation {reservation.id}")
            raise ValueError("Invalid reservation data")
        return True
