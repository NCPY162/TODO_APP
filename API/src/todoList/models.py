from django.db import models
from users.models import User 

class TodoList(models.Model):
    todo_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    user_id = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.description}, {self.created_at}"


