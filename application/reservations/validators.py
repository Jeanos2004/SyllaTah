from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

def validate_future_date(value):
    """
    Valide que la date est dans le futur.
    """
    if value <= timezone.now().date():
        raise ValidationError("La date doit être dans le futur.")


def validate_check_out_after_check_in(check_in, check_out):
    """
    Valide que la date de départ est après la date d'arrivée.
    """
    if check_out <= check_in:
        raise ValidationError("La date de départ doit être après la date d'arrivée.")


def validate_minimum_stay(check_in, check_out, minimum_days=1):
    """
    Valide que la durée du séjour est au moins égale au minimum requis.
    """
    if (check_out - check_in).days < minimum_days:
        raise ValidationError(f"La durée du séjour doit être d'au moins {minimum_days} jour(s).")


def validate_maximum_stay(check_in, check_out, maximum_days=30):
    """
    Valide que la durée du séjour ne dépasse pas le maximum autorisé.
    """
    if (check_out - check_in).days > maximum_days:
        raise ValidationError(f"La durée du séjour ne peut pas dépasser {maximum_days} jours.")


def validate_number_of_guests(value, maximum=10):
    """
    Valide que le nombre de personnes ne dépasse pas le maximum autorisé.
    """
    if value <= 0:
        raise ValidationError("Le nombre de personnes doit être supérieur à zéro.")
    if value > maximum:
        raise ValidationError(f"Le nombre de personnes ne peut pas dépasser {maximum}.")


def validate_at_least_one_service(accommodation, transport, activity):
    """
    Valide qu'au moins un service (hébergement, transport ou activité) est sélectionné.
    """
    if not any([accommodation, transport, activity]):
        raise ValidationError(
            "Vous devez sélectionner au moins un service (hébergement, transport ou activité)."
        )


def validate_reservation_period(check_in, check_out, accommodation=None, transport=None, activity=None):
    """
    Valide que la période de réservation est compatible avec les services sélectionnés.
    """
    # Validation de base des dates
    validate_future_date(check_in)
    validate_check_out_after_check_in(check_in, check_out)
    
    # Validation de la durée du séjour
    validate_minimum_stay(check_in, check_out)
    validate_maximum_stay(check_in, check_out)
    
    # Validation spécifique pour l'hébergement
    if accommodation:
        # Ici, vous pourriez ajouter des validations spécifiques à l'hébergement
        # Par exemple, vérifier la disponibilité de l'hébergement pour cette période
        pass
    
    # Validation spécifique pour le transport
    if transport:
        # Ici, vous pourriez ajouter des validations spécifiques au transport
        # Par exemple, vérifier que la date de transport est dans la période de réservation
        pass
    
    # Validation spécifique pour l'activité
    if activity:
        # Ici, vous pourriez ajouter des validations spécifiques à l'activité
        # Par exemple, vérifier que la date de l'activité est dans la période de réservation
        pass
