from django.urls import path # type: ignore
from .views.tasks_view \
        import CreateTaskAPIView, UpdateTaskAPIView, \
           GetAllTasksAPIView, GetOneTaskAPIView, DeleteTaskAPIView
from .views.task_status_view \
    import GetInProgessTaskAPIView, GetCompletedTasksAPIView, GetValidatedTasksAPIView
        

urlpatterns = [
    path('all/', view=GetAllTasksAPIView.as_view(), name="all_tasks"),
    path('task/', view=CreateTaskAPIView.as_view(), name="create_task"),
    path('task/<int:task_id>/task/', view=GetOneTaskAPIView.as_view(), name="one_task"),
    path('task/<int:task_id>/update_task/', view=UpdateTaskAPIView.as_view(), name="update_task"),
    path('task/<int:task_id>/delete_task/', view=DeleteTaskAPIView.as_view(), name="delete_task"),

    path('in_progress/', view=GetInProgessTaskAPIView.as_view(), name="inprogress_task"),
    path('completed/', view=GetCompletedTasksAPIView.as_view(), name="completed_task"),
    path('validated/', view=GetValidatedTasksAPIView.as_view(), name="validated_task"),
]
