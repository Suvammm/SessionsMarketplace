from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'USER', 'User'
        CREATOR = 'CREATOR', 'Creator'
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    role_selected = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
