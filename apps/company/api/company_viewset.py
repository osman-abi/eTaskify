from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.tasks.serializers import TaskSerializer
from permissions import IsAdmin
from ..models import Company
from ..serializers import CompanyCreateSerializer


class CompanyViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    ViewSet for creating a new company.
    """

    queryset = Company.objects.all()
    http_method_names = ["post", "get"]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """

        serializers = {
            "create": CompanyCreateSerializer,
            "tasks": TaskSerializer,
        }

        return serializers.get(self.action)

    def get_permissions(self):
        """
        Assign permissions based on the action.
        """
        if self.action == "create":
            self.permission_classes = [IsAdmin]
        self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Handle company creation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="tasks")
    def tasks(self, request, pk=None):
        """
        Handle GET requests to retrieve tasks for a specific company.
        """
        company = self.get_object()
        tasks = (
            company.tasks.all()
        )  # Assuming you have a related name 'tasks' in your Company model
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
