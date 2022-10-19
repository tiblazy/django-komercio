from django.db import models

from uuid import uuid4

from accounts.models import Account

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True,)
    
    seller = models.ForeignKey(Account, on_delete=models.CASCADE,)