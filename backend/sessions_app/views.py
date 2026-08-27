from django.db.models import Count, Q
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Session
from .permissions import IsCreator
from .serializers import SessionSerializer

def annotated(): return Session.objects.select_related('creator').annotate(active_booking_count=Count('bookings', filter=Q(bookings__status='ACTIVE')))

class SessionListCreateView(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
    def get_queryset(self): return annotated()
    def get_permissions(self): return [permissions.AllowAny()] if self.request.method == 'GET' else [IsCreator()]
    def perform_create(self, serializer): serializer.save(creator=self.request.user)

class SessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SessionSerializer
    def get_queryset(self): return annotated()
    def get_permissions(self): return [permissions.AllowAny()] if self.request.method == 'GET' else [IsCreator()]
    def perform_update(self, serializer):
        if serializer.instance.creator_id != self.request.user.id: raise PermissionDenied('You do not own this session.')
        serializer.save()
    def perform_destroy(self, instance):
        if instance.creator_id != self.request.user.id: raise PermissionDenied('You do not own this session.')
        instance.delete()

class CreatorSessionListView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsCreator]
    def get_queryset(self): return annotated().filter(creator=self.request.user)
