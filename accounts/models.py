from django.db import models
from django.contrib.auth.models import AbstractUser

from uuid import uuid4

class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    is_seller = models.BooleanField(default=False,) 
    
    REQUIRED_FIELDS = ['first_name', 'last_name',]