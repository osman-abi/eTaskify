from django.urls import path
from rest_framework.routers import DefaultRouter
from .api import (
    TaskViewSet,
)
router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')

urlpatterns = router.urls
