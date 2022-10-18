from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    is_seller = models.BooleanField(default=False,) 
    
    REQUIRED_FIELDS = ['first_name', 'last_name',]