from rest_framework import serializers # type: ignore
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    deleted_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    start_date = serializers.DateField(format="%d/%m/%Y", required=False)
    end_date = serializers.DateField(format="%d/%m/%Y", required=False)
    start_time = serializers.TimeField(format="%H:%M:%S", required=False)
    end_time = serializers.TimeField(format="%H:%M:%S", required=False)

    class Meta:
        model = Task
        fields = "__all__"
    
    def validate_status(self, value):
        if value not in ["en cours, terminé, validé"]:
            raise serializers.ValidationError({"message": "Le statut d'une tâche doit être 'en cours', 'terminé' ou 'validé'"})
        return value
    
    def validate(self, data):
        # Validation des dates
        if 'start_date' in data and data['start_date'] < timezone.now().date(): 
            raise serializers.ValidationError({"start_date": "La date de début de la tâche ne peut pas être antérieure à aujourd'hui"})
        
        if 'end_date' in data and data['end_date'] < timezone.now().date(): 
            raise serializers.ValidationError({"end_date": "La date de fin de la tâche ne peut pas être antérieure à aujourd'hui"})
        
        if 'start_date' in data and 'end_date' in data and data['start_date'] > data['end_date']:
            raise serializers.ValidationError({"message" : "La date de début doit être inférieure à celle de fin"})
        
        # Validation des heures
        if "start_time" in data and data['start_time'] < timezone.now().time(): 
            raise serializers.ValidationError({"start_time" : "L'heure de début de la tâche ne peut pas être antérieure à l'heure actuelle"})
        
        if "end_time" in data and data['end_time'] < timezone.now().time(): 
            raise serializers.ValidationError({"end_time" : "L'heure de fin de la tâche ne peut pas être antérieure à l'heure actuelle"})
        
        if 'start_time' in data and 'end_time' in data:
            if data['start_time'] > data['end_time']:
                raise serializers.ValidationError({"message" : "L'heure de début doit être inférieure à celle de fin"})
        
        return data
