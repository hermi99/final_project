from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Users(AbstractUser):
    full_name = models.CharField(max_length=100, null=True)
