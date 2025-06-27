from django.db import models

# Create your models here.
# accounts/models.py

from django.db import models

class User(models.Model):
    choices = (
        ('Employee', 'Employee'),
        ('HR', 'HR'),
        ('Admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # store hashed passwords manually
    position = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=50, default='Employee', choices=choices)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name.split(' ')[0]