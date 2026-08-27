from django.db.models import Count, Q
from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='creator.name', read_only=True)
    creator_id = serializers.IntegerField(source='creator.id', read_only=True)
    active_booking_count = serializers.IntegerField(read_only=True)
    remaining_seats = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = ('id', 'creator', 'creator_id', 'title', 'description', 'start_time', 'duration_minutes', 'capacity', 'active_booking_count', 'remaining_seats', 'created_at', 'updated_at')
        read_only_fields = ('id', 'creator', 'creator_id', 'active_booking_count', 'remaining_seats', 'created_at', 'updated_at')
    def get_remaining_seats(self, obj): return max(0, obj.capacity - getattr(obj, 'active_booking_count', 0))
