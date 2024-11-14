from django.db import models # type: ignore
from django.utils import timezone
from datetime import timedelta
from todoList.models import TodoList

class TaskManager(models.Manager):
    def in_progress_tasks(self):
        return self.filter(status='en cours')
    
    def completed_task(self):
        return self.filter(status='terminé')
    
    def validated_task(self):
        return self.filter(status='validé')
        
class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ("en cours", "En cours"),
        ("terminé", "Terminé"),
        ("validé", "Validé")
    ]

    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=TASK_STATUS_CHOICES)

    # Définir les valeurs par défaut à l'aide des fonctions définies ci-dessus
    start_date = models.DateField(default=timezone.now().date())
    end_date = models.DateField(default=timezone.now().date())
    start_time = models.TimeField(default=timezone.now().time().replace(second=0, microsecond=0))
    end_time = models.TimeField(default=timezone.now().time().replace(second=0, microsecond=0))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    todo_list = models.ForeignKey(TodoList, related_name="tasks", on_delete=models.CASCADE)

    objects = TaskManager()  # Manager personnalisé

    def __str__(self):
        return f"{self.title}, {self.description}"