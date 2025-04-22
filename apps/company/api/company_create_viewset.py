from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from permissions import IsAdmin
from ..models import Company
from ..serializers import CompanyCreateSerializer


class CompanyCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for creating a new company.
    """
    queryset = Company.objects.all()
    serializer_class = CompanyCreateSerializer
    permission_classes = [IsAdmin]  # Custom permission to check if the user is admin
    http_method_names = ['post']

    def get_serializer_context(self):
        """
        Add the request to the serializer context.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        """
        Handle company creation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
