from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api import UserRegisterViewSet, UserCreateStaffViewSet

# Create a router and register our viewset with it.
router = routers.DefaultRouter()
router.register(r'register', UserRegisterViewSet, basename='user-register')
router.register(r'create-staff', UserCreateStaffViewSet, basename='user-create-staff')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
