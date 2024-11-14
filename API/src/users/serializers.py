from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import re
from .models import User

class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    deleted_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = "__all__"
    
    def validate_password(self, value):
        if len(value) != 6:
            raise serializers.ValidationError({"password" : "Le mot de passe doit comporter exactement 6 caractères"}) 
        
        if not re.search(r'\d', value) or not re.search(r'[._@^*-]', value):
            raise serializers.ValidationError({"message":"Le mot de passe doit contenir au moins un chiffre et un caractère spécial (@_-^*)"})
        return value
    
    def create(self, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.password = make_password(validated_data.pop("password"))
        return super().update(instance, validated_data)
    
    

    
