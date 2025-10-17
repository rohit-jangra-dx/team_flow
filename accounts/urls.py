from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import RegisterCreateView

urlpatterns = [
    path('register/', RegisterCreateView.as_view(), name="register-create"),
    path('token/', TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token-refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name="token-verify"),    
]