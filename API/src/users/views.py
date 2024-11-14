from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from tokens.authentication import TokenAuthentication
from .serializers import UserSerializer
from .models import User

class CreateUserAPIView(APIView):
    def post(self, request):
        user = request.data
        if not user:
            return Response({"message": "Aucune donnée reçue"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            username = user.get('username')
            if username and User.objects.filter(username=username).exists():
                return Response({"message":"Cet utilisateur existe déjà en base"},
                                status=status.HTTP_409_CONFLICT)
            
            serializer = UserSerializer(data=user)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Utilisateur créé avec succès"}, 
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Echec de création de l'utilisateur", "errors": serializer.errors}, 
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":"Une erreur est survenue", "errors": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAllUsersAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            users = User.objects.all()
            if users.exists():
                serializer = UserSerializer(users, many=True)
                return Response({"message": "Les données utilisateur ont été récupérées avec succès", 
                             "users": serializer.data}, 
                            status=status.HTTP_200_OK)
            else: 
                return Response({"message": "Aucune donnée utilisateur trouvée en base"},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":"Une erreur est survenue", "errors": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetOneUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            serializer = UserSerializer(user)
            return Response({"message": "Donnée utilisateur récupérée avec succès", "user": serializer.data},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "L'utilisateur demandée n'existe pas en base"}, 
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":"Une erreur est survenue", "errors": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        try:
            existing_user = User.objects.get(user_id=user_id)
            serializer = UserSerializer(existing_user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Donnée utilisateur mise à jour avec succès"}, 
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "Echec de mise à jour de l'utilisateur", "errors": serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "La donnée utilisateur à mettre à jour n'existe pas en base"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":"Une erreur est survenue", "errors": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            user.delete()
            return Response({"message": "Donnée utilisateur supprimée avec succès"},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "La donnée utilisateur à supprimer n'existe pas"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":"Une erreur est survenue", "errors": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)