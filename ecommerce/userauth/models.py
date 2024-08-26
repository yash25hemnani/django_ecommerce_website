from django.db import models
# Creating Custom User Model
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=200)
    bio = models.CharField(max_length=200, null=True)

    USERNAME_FIELD = "email" # Changes the initial username field to email
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username