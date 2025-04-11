import stripe
from django.conf import settings
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePaymentManager:
    @staticmethod
    def create_payment_intent(reservation):
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(reservation.total_amount * 100),  # Conversion en centimes
                currency='eur',
                metadata={
                    'reservation_id': str(reservation.id),
                    'customer_email': reservation.email,
                    'lodge_id': str(reservation.lodge_id)
                }
            )
            return intent
        except stripe.error.StripeError as e:
            raise Exception(f"Erreur Stripe: {str(e)}")

    @staticmethod
    def confirm_payment(payment_intent_id):
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if intent.status == 'succeeded':
                return True
            return False
        except stripe.error.StripeError as e:
            raise Exception(f"Erreur lors de la confirmation: {str(e)}")