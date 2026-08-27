from django.db import IntegrityError, transaction
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from sessions_app.models import Session
from .models import Booking
from .serializers import BookingSerializer

class BookSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            with transaction.atomic():
                session = Session.objects.select_for_update().get(pk=pk)
                if session.start_time <= timezone.now():
                    return Response({'detail': 'This session has already started.'}, status=status.HTTP_409_CONFLICT)
                if Booking.objects.filter(user=request.user, session=session, status=Booking.Status.ACTIVE).exists():
                    return Response({'detail': 'You already have an active booking.'}, status=status.HTTP_409_CONFLICT)
                active = Booking.objects.filter(session=session, status=Booking.Status.ACTIVE).count()
                if active >= session.capacity:
                    return Response({'detail': 'This session is full.'}, status=status.HTTP_409_CONFLICT)
                booking = Booking.objects.create(user=request.user, session=session)
        except Session.DoesNotExist:
            return Response({'detail': 'Session not found.'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'detail': 'You already have an active booking.'}, status=status.HTTP_409_CONFLICT)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return Booking.objects.filter(user=self.request.user).select_related('session__creator').annotate(active_booking_count=Count('session__bookings', filter=Q(session__bookings__status='ACTIVE')))
