from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [path('admin/', admin.site.urls), path('api/', include('users.urls')), path('api/', include('sessions_app.urls')), path('api/', include('bookings.urls')), path('api/auth/token/refresh/', TokenRefreshView.as_view())]
