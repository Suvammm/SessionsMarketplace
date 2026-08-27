from django.urls import path
from .views import GoogleLoginView, MeView, PasswordLoginView, RoleSelectionView
urlpatterns = [path('auth/me/', MeView.as_view()), path('auth/profile/', MeView.as_view()), path('auth/google/', GoogleLoginView.as_view()), path('auth/login/', PasswordLoginView.as_view()), path('auth/role/', RoleSelectionView.as_view())]
