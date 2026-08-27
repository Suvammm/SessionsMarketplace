from google.auth.transport import requests
from google.oauth2 import id_token
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import GoogleLoginSerializer, PasswordLoginSerializer, RoleSelectionSerializer, UserSerializer

def token_response(user):
    refresh = RefreshToken.for_user(user)
    return Response({'access': str(refresh.access_token), 'refresh': str(refresh), 'user': UserSerializer(user).data})

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self): return self.request.user

class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        payload = GoogleLoginSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        if not settings.GOOGLE_CLIENT_ID:
            raise ValidationError({'detail': 'Google OAuth is not configured.'})
        try:
            info = id_token.verify_oauth2_token(payload.validated_data['id_token'], requests.Request(), settings.GOOGLE_CLIENT_ID)
        except ValueError:
            return Response({'detail': 'Google sign-in failed.'}, status=status.HTTP_401_UNAUTHORIZED)
        if not info.get('email') or not info.get('email_verified'):
            return Response({'detail': 'Google account email is not verified.'}, status=status.HTTP_401_UNAUTHORIZED)
        user, created = User.objects.get_or_create(email=info['email'], defaults={'username': info['email'], 'name': info.get('name', '')})
        if not created and info.get('name') and not user.name:
            user.name = info['name']; user.save(update_fields=['name'])
        return token_response(user)

class PasswordLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        payload = PasswordLoginSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        user = authenticate(request, username=payload.validated_data['username'], password=payload.validated_data['password'])
        if not user:
            return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        return token_response(user)

class RoleSelectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RoleSelectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.role_selected:
            return Response({'detail': 'Your role has already been selected.'}, status=status.HTTP_409_CONFLICT)
        request.user.role = serializer.validated_data['role']
        request.user.role_selected = True
        request.user.save(update_fields=['role', 'role_selected'])
        return Response(UserSerializer(request.user).data)
