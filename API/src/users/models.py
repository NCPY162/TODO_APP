from django.db import models
from django.contrib.auth.hashers import check_password

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=128)
    address = models.CharField(max_length=255, null=True)
    zipcode = models.IntegerField(max_length=5, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.email}"
    
    def check_pass(self, raw_password):
        return check_password(raw_password, self.password)
    
    def is_authenticated(self):
        return True