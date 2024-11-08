from rest_framework import serializers
from .models import TodoList

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        created_at = serializers.DateTimeField(format="%d%m%Y %H:%M:%S", read_only=True)
        updated_at = serializers.DateTimeField(format="%d%m%Y %H:%M:%S", read_only=True)
        deleted_at = serializers.DateTimeField(format="%d%m%Y %H:%M:%S", read_only=True)
        
        model = TodoList
        fields = "__all__"