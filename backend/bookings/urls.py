from django.urls import path
from .views import BookSessionView, BookingListView
urlpatterns = [path('sessions/<int:pk>/book/', BookSessionView.as_view()), path('bookings/', BookingListView.as_view())]
