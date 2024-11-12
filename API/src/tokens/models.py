from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import User
import binascii
import os

class Token(models.Model):
    access_token = models.CharField(max_length=255, primary_key=True)
    refresh_token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token_expiry = models.DateTimeField()
    refresh_token_expiry = models.DateTimeField()

    @staticmethod
    def generate_token():
        return binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):
        if not self.access_token:
            self.access_token = self.generate_token()
            self.access_token_expiry = timezone.now() + timedelta(minutes=45)
        
        if not self.refresh_token:
            self.refresh_token = self.generate_token()
            self.refresh_token_expiry = timezone.now() + timedelta(days=7)
        
        super().save(*args, **kwargs)
    
    def is_access_token_expired(self):
        return timezone.now() >= self.access_token_expiry

    def is_refresh_token_expired(self):
        return timezone.now() >= self.refresh_token_expiry

