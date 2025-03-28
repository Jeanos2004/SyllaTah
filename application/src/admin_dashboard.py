from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from reservations.models import Reservation, Payment  # Vérifiez que ce chemin est correct

@staff_member_required
def admin_dashboard(request):
    try:
        # Ajout d'un bloc try-except pour déboguer
        total_reservations = Reservation.objects.count()
        confirmed_reservations = Reservation.objects.filter(status='confirmed').count()
        pending_reservations = Reservation.objects.filter(status='pending').count()
        
        monthly_revenue = Payment.objects.filter(
            status='completed'
        ).annotate(
            month=TruncMonth('payment_date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')

        service_stats = {
            'accommodation': Reservation.objects.exclude(accommodation=None).count(),
            'transport': Reservation.objects.exclude(transport=None).count(),
            'activity': Reservation.objects.exclude(activity=None).count(),
        }

        context = {
            'total_reservations': total_reservations,
            'confirmed_reservations': confirmed_reservations,
            'pending_reservations': pending_reservations,
            'monthly_revenue': list(monthly_revenue),
            'service_stats': service_stats,
        }
        
        return render(request, 'admin/dashboard.html', context)
    except Exception as e:
        print(f"Erreur dans le dashboard : {str(e)}")
        return render(request, 'admin/dashboard.html', {
            'error': str(e),
            'total_reservations': 0,
            'confirmed_reservations': 0,
            'pending_reservations': 0,
            'monthly_revenue': [],
            'service_stats': {'accommodation': 0, 'transport': 0, 'activity': 0}
        })