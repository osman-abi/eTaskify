from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Task
from ..serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    TaskUpdateSerializer,
    TaskAssignSerializer,
)


class TaskViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset for creating and deleting tasks.
    """

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        serializers = {
            "create": TaskCreateSerializer,
            "partial_update": TaskUpdateSerializer,
            "assign": TaskAssignSerializer,
        }
        return serializers.get(self.action, TaskSerializer)

    def create(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new task instance.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a task instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Update a task instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a task instance.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'], url_path='assign')
    def assign(self, request, *args, **kwargs):
        """
        Assign users to a task. Request data should contain a list of user IDs to assign to the task.
        """
        print("request.data >>>> ", request.data)
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
