from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status 
from drf_yasg.utils import swagger_auto_schema
from tokens.authentication import TokenAuthentication
from ..serializers import TaskSerializer 
from ..models import Task 

class CreateTaskAPIView(APIView):
    """
        post:
        Créer une nouvelle tâche.

        - title : Titre de la tâche (string)
        - description : Description de la tâche (string)
        - status : Statut de la tâche (string, options : 'en cours', 'terminé', 'validé')
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Méthode permettant de créer une tâche",
        responses={201: TaskSerializer}
    )
    def post(self, request):
        try:
            task = request.data
            
            if not task:
                return Response({"message":"Aucune donnée reçue"},
                                status=status.HTTP_400_BAD_REQUEST)
            
            task_title = task.get('title')
            if task_title and Task.objects.filter(title=task_title).exists():
                return Response({"message": "Cette tâche existe déjà"}, 
                                 status=status.HTTP_409_CONFLICT)
            
            serializer = TaskSerializer(data=task)

            if serializer.is_valid():
                serializer.save()
                return Response({'message' : 'Tâche créée avec succès'}, 
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'message' : 'La création de la tâche a échoué', 
                                 'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)     
        except Exception as e:
                return Response({'message':'Une erreur est survenue', 'errors': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Get tasks datas
class GetAllTasksAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = Task.objects.all()
            if tasks.exists():
                serializer = TaskSerializer(tasks, many=True)
                return Response({'message': 'Données récupérées avec succès', 'tasks': serializer.data},
                               status=status.HTTP_200_OK)
            else:
                return Response({'message' : 'Aucune donnée trouvée en base'},
                                status=status.HTTP_404_NOT_FOUND)      
        except Exception as e:
            return Response({'message' : 'Une erreur est survenue', 'errors': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Get one task data
class GetOneTaskAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = Task.objects.get(task_id=task_id)
            serializer = TaskSerializer(task)
            return Response({'message': 'Donnée récupérée avec succès', 'task': serializer.data},
                               status=status.HTTP_200_OK)
        except Task.DoesNotExist :
                return Response({'message' : 'La donnée demandée n\'existe pas'},
                                status=status.HTTP_404_NOT_FOUND)   
        except Exception as e:
            return Response({'message' : 'Une erreur est survenue', 'errors': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Update task data
class UpdateTaskAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        try:
            existing_task = Task.objects.get(task_id=task_id)
            serializer = TaskSerializer(existing_task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'La tâche a été mise à jour avec succès'}, 
                                    status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Merci de vérifier les données fournies pour la mise à jour', 
                                 "errors": serializer.errors}, 
                                    status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
             return Response({'message' : 'La donnée à mettre à jour n\'existe pas'},
                                status=status.HTTP_404_NOT_FOUND)   
        except Exception as e:
             return Response({'message' : 'Une erreur est survenue', 'errors': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Delete task data
class DeleteTaskAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, task_id):
        try:
            existing_task = Task.objects.get(task_id=task_id)
            existing_task.delete()
            return Response({'message': 'La tâche a été supprimée avec succès'}, 
                            status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'message':'La donnée à supprimer n\'existe pas'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message':'Une erreur est survenue', 'errors': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        