from django.conf import settings
from django.db import models
from django.db.models import Q

class Booking(models.Model):
    class Status(models.TextChoices): ACTIVE = 'ACTIVE', 'Active'; CANCELLED = 'CANCELLED', 'Cancelled'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    session = models.ForeignKey('sessions_app.Session', on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'session'], condition=Q(status='ACTIVE'), name='unique_active_booking')]
        ordering = ['-created_at']
