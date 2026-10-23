from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True,max_length=15)

    ROLE_CHOICE=[
        ("customer", "Customer"),
        ("admin", "Admin"),
    ]
    role = models.CharField(choices=ROLE_CHOICE,max_length=12,default="customer")
    def __str__(self):
        return self.username