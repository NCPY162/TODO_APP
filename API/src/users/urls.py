from django.urls import path
from .views import CreateUserAPIView, GetAllUsersAPIView, GetOneUserAPIView, UpdateUserAPIView, DeleteUserAPIView

urlpatterns = [
    path("all/", view=GetAllUsersAPIView.as_view(), name="users"),
    path("user/", view=CreateUserAPIView.as_view(), name="user"),
    path("user/<int:user_id>/user/", view=GetOneUserAPIView.as_view(), name="one_user"),
    path("user/<int:user_id>/update_user/", view=UpdateUserAPIView.as_view(), name="update_user"),
    path("user/<int:user_id>/delete_user/", view=DeleteUserAPIView.as_view(), name="delete_user")
]
