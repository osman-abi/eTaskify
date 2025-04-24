from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api import UserViewSet

# Create a router and register our viewset with it.
router = routers.DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="user_login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
