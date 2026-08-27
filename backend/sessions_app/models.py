from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

class Session(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['start_time']
