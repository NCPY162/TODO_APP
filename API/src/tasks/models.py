from django.db import models # type: ignore
from django.utils import timezone
from datetime import timedelta

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
        ("terminé", "terminé"),
        ("validé", "Validé")
    ]

    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=TASK_STATUS_CHOICES)
    
    # Méthode pour obtenir la date actuelle
    def get_current_date():
        return timezone.now().date()
    
    # Méthode pour obtenir la date du jour suivant
    def get_next_day():
        return timezone.now().date() + timedelta(days=1)
    
    # Méthode pour obtenir l'heure actuelle
    def get_current_time():
        return timezone.now().time()
    
    # Méthode pour obtenir l'heure actuelle + 1h
    def get_time_plus_one_hour():
        return (timezone.now() + timedelta(hours=1)).time()

    # Définir les valeurs par défaut à l'aide des fonctions définies ci-dessus
    start_date = models.DateField(default=get_current_date)
    end_date = models.DateField(default=get_next_day)
    start_time = models.TimeField(default=get_current_time)
    end_time = models.TimeField(default=get_time_plus_one_hour)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = TaskManager()  # Manager personnalisé