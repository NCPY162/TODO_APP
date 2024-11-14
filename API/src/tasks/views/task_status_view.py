from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from tokens.authentication import TokenAuthentication # type: ignore
from ..serializers import TaskSerializer # type: ignore
from ..models import Task # type: ignore

class GetInProgessTaskAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            in_progress = Task.objects.in_progress_tasks()
            serializer = TaskSerializer(in_progress, many=True)
            if in_progress :
                return Response({'message': 'Tâches en cours récupérées avec succès', 
                                 'tasks_in_progress': serializer.data}, 
                                 status=status.HTTP_200_OK)
            else: 
                return Response({'message': 'Aucune tâche en cours n\'est disponible en base'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Une erreur est survenue', 'errors': str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCompletedTasksAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            completed_tasks = Task.objects.completed_task()
            serializer = TaskSerializer(completed_tasks, many=True)

            if completed_tasks:
                return Response({'message': 'Tâches terminées récupérées avec succès', 
                                'completed_tasks': serializer.data}, 
                                status=status.HTTP_200_OK)
            else: 
                return Response({'message': 'Aucune tâche terminée n\'est disponible en base'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Une erreur est survenue', 'errors': str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetValidatedTasksAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            validated_tasks = Task.objects.validated_task()
            serializer = TaskSerializer(validated_tasks, many=True)
            if validated_tasks:
                return Response({'message': 'Tâches validées récupérées avec succès', 
                                'validated_tasks': serializer.data}, 
                                status=status.HTTP_200_OK)
            else: 
                return Response({'message': 'Aucune tâche validée n\'est disponible en base'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Une erreur est survenue', 'errors': str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

