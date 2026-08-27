from django.urls import path
from .views import CreatorSessionListView, SessionDetailView, SessionListCreateView
urlpatterns = [path('sessions/', SessionListCreateView.as_view()), path('sessions/<int:pk>/', SessionDetailView.as_view()), path('creator/sessions/', CreatorSessionListView.as_view())]
