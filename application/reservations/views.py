from requests import Response
from rest_framework import viewsets
from .models import Reservation
from .serializers import ReservationSerializer
from .permissions import ReservationPermissions
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [ReservationPermissions]  # Utilisation de notre permission personnalisée
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

    """ @action(detail=True, methods=['get'])
    @method_decorator(login_required)
    def generate_pdf(self, request, pk=None):
        reservation = self.get_object()
        
        # Vérifier que l'utilisateur est autorisé
        if reservation.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "Not authorized"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Charger le template
        template = get_template('reservations/reservation_pdf.html')
        html = template.render({'reservation': reservation})

        # Créer le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reservation_{reservation.id}.pdf"'
        
        # Générer PDF
        pisa.CreatePDF(html, dest=response)
        return response
 """
    @action(detail=True, methods=['get'])
    def view_receipt(self, request, pk=None):
        """View receipt in browser"""
        reservation = self.get_object()
        
        if reservation.user != request.user and not request.user.is_staff:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        context = {
            'reservation_id': reservation.id,
            'reservation_date': reservation.check_in_date,
            'user_name': reservation.user.get_full_name(),
            'service_type': reservation.service_type,
            'check_in_date': reservation.check_in_date,
            'check_out_date': reservation.check_out_date,
            'reservation_date': reservation.reservation_date,
            'total_price': reservation.total_price,
            'reservation_id': reservation.id,
        }
        
        template = get_template('reservations/reservation_pdf.html')
        html = template.render(context)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="receipt.pdf"'
        pisa.CreatePDF(html, dest=response)
        return response

    @action(detail=True, methods=['get'])
    def download_receipt(self, request, pk=None):
        """Download receipt as attachment"""
        reservation = self.get_object()
        
        if reservation.user != request.user and not request.user.is_staff:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        context = {
            'reservation': reservation,
            'user_name': reservation.user.get_full_name(),
            'service_type': reservation.service_type,
            'check_in_date': reservation.check_in_date,
            'check_out_date': reservation.check_out_date,
            'reservation_date': reservation.reservation_date,
            'total_price': reservation.total_price,
            'reservation_id': reservation.id,
        }

        template = get_template('reservations/reservation_pdf.html')
        html = template.render(context)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reservation_{reservation.id}.pdf"'
        pisa.CreatePDF(html, dest=response)
        return response

    @action(detail=True, methods=['post'])
    def save_to_wallet(self, request, pk=None):
        """Save receipt to user's wallet"""
        reservation = self.get_object()
        
        if reservation.user != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        # Add to user's wallet (you'll need to implement this model)
        UserWallet.objects.create(
            user=request.user,
            reservation=reservation,
            receipt_type='reservation'
        )
        
        return Response({"message": "Receipt saved to wallet"}, status=status.HTTP_200_OK)