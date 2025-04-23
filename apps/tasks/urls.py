from django.urls import path
from rest_framework.routers import DefaultRouter
from .api import (
    TaskViewSet,
    TaskUpdateViewSet,
    TaskAssignViewSet,
)
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'tasks/update', TaskUpdateViewSet, basename='task-update')
router.register(r'tasks/assign', TaskAssignViewSet, basename='task-assign')
