from django.urls import path
from .views import CreateTodoListAPIView, GetAllTodosAPIView, GetOneTodoAPIView,\
                    UpdateTodoListAPIView, DeleteTodoListAPIView
urlpatterns = [
    path("todo/", view=CreateTodoListAPIView.as_view(), name="todo"),
    path("todos/", view=GetAllTodosAPIView.as_view(), name="todos"),
    path("todo/<int:todo_id>/todo/", view=GetOneTodoAPIView.as_view(), name="one_todo"),
    path("todo/<int:todo_id>/update_todo/", view=UpdateTodoListAPIView.as_view(), name="update_todo"),
    path("todo/<int:todo_id>/delete_todo/", view=DeleteTodoListAPIView.as_view(), name="delete_todo")
]
