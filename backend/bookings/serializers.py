from rest_framework import serializers
from .models import Booking
from sessions_app.serializers import SessionSerializer
class BookingSerializer(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ('id', 'session', 'status', 'created_at')
