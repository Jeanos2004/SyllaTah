from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import os

@shared_task
def clean_monitoring_logs():
    log_file = "app_monitoring.log"
    backup_file = f"app_monitoring_{timezone.now().strftime('%Y%m%d')}.log"
    
    # Créer une copie de sauvegarde
    if os.path.exists(log_file):
        os.rename(log_file, backup_file)
        
    # Supprimer les anciennes sauvegardes (plus de 4 semaines)
    old_date = timezone.now() - timedelta(weeks=4)
    for file in os.listdir():
        if file.startswith("app_monitoring_"):
            file_date = timezone.datetime.strptime(file.split('_')[2].split('.')[0], '%Y%m%d')
            if file_date.date() < old_date.date():
                os.remove(file)