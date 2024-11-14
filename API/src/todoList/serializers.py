from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import TodoList
import re

class TodoListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m%/Y %H:%M:%S", read_only=True)
    deleted_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    
    class Meta:
        model = TodoList
        fields = "__all__"

    def validate_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError({"name": "Ce champ doit correspondre à une chaîne de caractères"})

        if re.match(r'^\d+$', value):
            raise serializers.ValidationError({"name": "Ce champ ne doit pas contenir uniquement de valeurs numériques"})
        
        return value
