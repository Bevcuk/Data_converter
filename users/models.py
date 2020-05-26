from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, BaseUserManager


class DataOceanUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
