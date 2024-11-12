from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from users.models import User
from tokens.models import Token
from datetime import timedelta

class ObtainTokenView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
    
        try:
            user = User.objects.get(username=username)
            if user.check_pass(password):
                token, created = Token.objects.get_or_create(user=user)

                if not created and token.is_access_token_expired():
                    token.access_token = Token.generate_token()
                    token.access_token_expiry = timezone.now() + timedelta(minutes=45)
                    token.save()

                return Response({"access_token" : token.access_token,
                                 "access_token_expiry": token.access_token_expiry,
                                 "refresh_token": token.refresh_token,
                                 "refresh_token_expiry": token.refresh_token_expiry}, status=status.HTTP_200_OK)
            
            return Response({"message": "Mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"message": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        try:
            token = Token.objects.get(refresh_token=refresh_token)

            if token.is_refresh_token_expired():
                token.delete()
                return Response({"message": "Le refresh token a expiré"}, status=status.HTTP_401_UNAUTHORIZED)
            
            token.access_token = Token.generate_token()
            token.access_token_expiry = timezone.now() + timedelta(minutes=45)

            return Response({
                "access_token": token.access_token,
                "access_token_expiry" : token.access_token_expiry
            }, status=status.HTTP_200_OK)
        
        except Token.DoesNotExist:
            return Response({"message": "Resfresh token invalide"}, status=status.HTTP_404_NOT_FOUND)

