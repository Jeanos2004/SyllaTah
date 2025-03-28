from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.cache import cache

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérification de l'en-tête User-Agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if not user_agent:
            return HttpResponseForbidden('User-Agent requis')

        # Vérification des requêtes par IP
        ip = request.META.get('REMOTE_ADDR')
        requests_key = f'requests_per_minute_{ip}'
        requests_count = cache.get(requests_key, 0)

        if requests_count > 60:  # 60 requêtes par minute maximum
            return HttpResponseForbidden('Trop de requêtes')

        cache.set(requests_key, requests_count + 1, timeout=60)

        # Vérification de la session active
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                if (timezone.now() - last_activity).seconds > 3600:  # 1 heure
                    request.session.flush()
                    
            request.session['last_activity'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response