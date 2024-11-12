from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Token

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.headers.get("Authorization").split("Bearer ")[-1]
        if not access_token:
            return None
        
        try:
            token = Token.objects.get(access_token=access_token)

            if token.is_access_token_expired():
                raise AuthenticationFailed("Token expiré")
            return (token.user, token)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Token invalide")