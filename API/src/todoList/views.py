from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TodoListSerializer
from .models import TodoList

class CreateTodoListAPIView(APIView):
    def post(self, request):
        todo = request.data
        try:
            if not todo:
                return Response({"message": "Aucune donnée n'a été reçue"}, 
                                status=status.HTTP_400_BAD_REQUEST)
              
            todo_name = todo.get("name")
            if todo_name and TodoList.objects.filter(name=todo_name).exists():
                return Response({"message": "Cette todo existe déjà"}, 
                                status=status.HTTP_409_CONFLICT)
            
            serializer = TodoListSerializer(data=todo)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "La todo a été créée avec succès"}, 
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Echec de création de la todo, merci de vérifier les valeurs fournies",
                                "errors" : serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":"Une erreur est survenue", "errors":str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAllTodosAPIView(APIView):
    def get(self, request):
        try:
            todos = TodoList.objects.all()
            if todos.exists():
                serializer = TodoListSerializer(todos, many=True)
                return Response({"message":"Les todos ont été récupérés avec succès", "todos":serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "Aucune donnée todos trouvée en base"}, 
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":"Une erreur est survenue", "errors":str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetOneTodoAPIView(APIView):
    def get(self, request, todo_id):
        try:
            todo = TodoList.objects.get(todo_id=todo_id)
            serializer = TodoListSerializer(todo)
            return Response({"message" : "Données todos récupérées avec succès", "todo": serializer.data},
                                status=status.HTTP_200_OK)  
        except TodoList.DoesNotExist : 
            return Response({"message":"La todo demandée est introuvable"}, 
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":"Une erreur est survenue", "errors":str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateTodoListAPIView(APIView):
    def put(self, request, todo_id):
        try:
            todo = request.data
            existing_todo = TodoList.objects.get(todo_id=todo_id)
            serializer = TodoListSerializer(existing_todo, data=todo, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Donnée todo mise à jour avec succès"},
                            status=status.HTTP_200_OK)
            else:
                return Response({"message": "Echec de mise à jour! Merci de vérifier les données fournies"},
                                status=status.HTTP_400_BAD_REQUEST)
        except TodoList.DoesNotExist:
            return Response({"message" : "La todo à mettre à jour n'existe pas"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":"Une erreur est survenue", "errors":str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class DeleteTodoListAPIView(APIView):
    def delete(self, request, todo_id):
        try:
            todo = TodoList.objects.get(todo_id=todo_id)
            todo.delete()
            return Response({"message":"La todo a été supprimée avec succès"}, 
                            status=status.HTTP_200_OK)
        except TodoList.DoesNotExist:
            return Response({"message": "La todo que vous tentez de supprimer n'existe pas"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":"Une erreur est survenue", "errors":str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)