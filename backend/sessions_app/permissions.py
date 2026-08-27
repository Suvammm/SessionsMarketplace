from rest_framework.permissions import BasePermission
from users.models import User
class IsCreator(BasePermission):
    message = 'Creator role required.'
    def has_permission(self, request, view): return bool(request.user.is_authenticated and request.user.role == User.Role.CREATOR)
