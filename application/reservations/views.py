from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Reservation, Payment
from .serializers import ReservationSerializer
from .permissions import ReservationPermissions
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import io
from rest_framework.views import APIView
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class ReservationViewSet(viewsets.ModelViewSet):
    """
    Vue principale pour la gestion des réservations.
    Permet les opérations CRUD et des actions personnalisées.
    """
    permission_classes = [ReservationPermissions]  # Gestion des permissions d'accès
    queryset = Reservation.objects.all()  # Récupère toutes les réservations
    serializer_class = ReservationSerializer  # Sérialiseur pour la conversion des données
    
    # Configuration des filtres et de la recherche
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['reservation_number', 'status']  # Champs recherchables
    ordering_fields = ['reservation_date', 'check_in_date', 'total_price']  # Champs pour le tri
    ordering = ['-reservation_date']  # Tri par défaut (du plus récent au plus ancien)

    def perform_create(self, serializer):
        """
        Méthode de création d'une réservation avec calcul automatique du prix.
        Utilise une transaction atomique pour garantir l'intégrité des données.
        """
        with transaction.atomic():
            reservation = serializer.save(user=self.request.user)
            reservation.calculate_total_price()
            
            try:
                # Préparation du contexte pour le template
                context = {
                    'reservation': reservation,
                    'user_name': reservation.user.get_full_name() or reservation.user.username,
                    'total_price': reservation.total_price,
                    'reservation_number': reservation.reservation_number
                }

                # Génération du PDF
                template = get_template('reservations/reservation_pdf.html')
                html = template.render(context)
                pdf_file = io.BytesIO()
                pisa.CreatePDF(html, dest=pdf_file)
                pdf_file.seek(0)

                # Préparation et envoi de l'email
                subject = f'Confirmation de votre réservation #{reservation.reservation_number}'
                html_message = render_to_string('email/reservation_confirmation.html', context)
                plain_message = strip_tags(html_message)

                email = EmailMessage(
                    subject=subject,
                    body=plain_message,
                    from_email='noreply@syllatah.com',
                    to=[reservation.user.email],
                )
                email.attach(f'reservation_{reservation.reservation_number}.pdf', 
                           pdf_file.getvalue(), 'application/pdf')
                email.send()

                # Log de l'email
                from .models import EmailLog
                EmailLog.objects.create(
                    reservation=reservation,
                    email_type='confirmation',
                    recipient=reservation.user.email,
                    subject=subject,
                    body=plain_message
                )

            except Exception as e:
                print(f"Erreur lors de l'envoi de l'email: {str(e)}")

            reservation.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Endpoint pour annuler une réservation.
        Nécessite une raison d'annulation et met à jour le statut.
        """
        reservation = self.get_object()
        reason = request.data.get('reason', '')
        
        try:
            reservation.cancel_reservation(reason)
            return Response({'status': 'Reservation cancelled'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        """
        Gestion des paiements pour une réservation.
        - Vérifie si la réservation n'est pas annulée
        - Traite le paiement
        - Met à jour le statut de la réservation si payée en totalité
        """
        reservation = self.get_object()
        
        if reservation.status == 'cancelled':
            return Response(
                {'error': 'Cannot process payment for cancelled reservation'},
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = request.data.get('amount')
        if not amount:
            return Response(
                {'error': 'Payment amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                # Création de l'enregistrement du paiement
                payment = Payment.objects.create(
                    reservation=reservation,
                    amount=amount,
                    payment_type=request.data.get('payment_type', 'card')
                )
                
                # Mise à jour du montant payé et du statut
                reservation.amount_paid += payment.amount
                if reservation.amount_paid >= reservation.total_price:
                    reservation.status = 'confirmed'
                reservation.save()
                
                return Response({'status': 'Payment processed successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def view_receipt(self, request, pk=None):
        """
        Affichage du reçu PDF dans le navigateur.
        Génère un PDF avec les détails de la réservation et les informations de paiement.
        """
        reservation = self.get_object()
        
        # Vérification des permissions
        if reservation.user != request.user and not request.user.is_staff:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        # Préparation des données pour le PDF
        context = {
            'reservation': reservation,
            'user_name': reservation.user.get_full_name(),
            'service_type': reservation.service_type,
            'check_in_date': reservation.check_in_date,
            'check_out_date': reservation.check_out_date,
            'reservation_date': reservation.reservation_date,
            'total_price': reservation.total_price,
            'amount_paid': reservation.amount_paid,
            'payment_status': reservation.payment_status,
            'reservation_number': reservation.reservation_number
        }
        
        # Génération du PDF
        template = get_template('reservations/reservation_pdf.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="receipt.pdf"'
        pisa.CreatePDF(html, dest=response)
        return response

    @action(detail=True, methods=['get'])
    def download_receipt(self, request, pk=None):
        """
        Téléchargement du reçu PDF.
        Similaire à view_receipt mais force le téléchargement au lieu de l'affichage.
        """
        # [Code similaire à view_receipt avec modification du Content-Disposition]

    @action(detail=True, methods=['post'])
    def save_to_wallet(self, request, pk=None):
        """
        Sauvegarde du reçu dans le portefeuille numérique de l'utilisateur.
        Permet un accès rapide aux reçus précédents.
        """
        reservation = self.get_object()
        
        if reservation.user != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        UserWallet.objects.create(
            user=request.user,
            reservation=reservation,
            receipt_type='reservation'
        )
        
        return Response({"message": "Receipt saved to wallet"}, status=status.HTTP_200_OK)


class ReservationPaymentView(APIView):
    def post(self, request, reservation_id):
        reservation = Reservation.objects.get(id=reservation_id)
        
        try:
            # Créer l'intention de paiement Stripe
            intent = stripe.PaymentIntent.create(
                amount=int(reservation.total_amount * 100),  # Stripe utilise les centimes
                currency='eur',
                metadata={'reservation_id': reservation.id}
            )
            
            reservation.update_payment_status('pending', intent.id)
            
            return Response({
                'clientSecret': intent.client_secret,
                'reservation_id': reservation.id
            })
            
        except stripe.error.StripeError as e:
            return Response({
                'error': str(e)
            }, status=400)

    def patch(self, request, reservation_id):
        reservation = Reservation.objects.get(id=reservation_id)
        new_status = request.data.get('payment_status')
        
        if new_status not in dict(Reservation.PAYMENT_STATUS):
            return Response({'error': 'Statut de paiement invalide'}, status=400)
            
        reservation.update_payment_status(new_status)
        return Response({'status': 'updated'})