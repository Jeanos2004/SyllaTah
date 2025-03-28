from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .serializers import TokenValidationSerializer

def validate_token_and_lodge(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        lodge_id = kwargs.get('lodge_id')

        serializer = TokenValidationSerializer(data={
            'token': token,
            'lodge_id': lodge_id
        })

        if not serializer.is_valid():
            return Response({
                'detail': 'Token invalide ou non autorisé pour ce lodge'
            }, status=status.HTTP_403_FORBIDDEN)

        request.validated_user = serializer.validated_data['user']
        return view_func(self, request, *args, **kwargs)

    return wrapper