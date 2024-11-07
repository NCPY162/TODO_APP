from rest_framework import serializers # type: ignore
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        created_at = serializers.DateTimeField(format="%d%m%Y %H:%M:%S", read_only=True)
        updated_at = serializers.DateTimeField(format="%d%m%Y %H:%M:%S", read_only=True)
        deleted_at = serializers.DateTimeField(format="%d%m%Y %H:%M:%S", read_only=True)
        start_date = serializers.DateField(format="%d%m%Y", read_only=True)
        end_date = serializers.DateField(format="%d%m%Y", read_only=True)
        start_time = serializers.TimeField(format="%H:%M:%S", read_only=True)
        end_time = serializers.TimeField(format="%H:%M:%S", read_only=True)

        model = Task
        fields = "__all__"
