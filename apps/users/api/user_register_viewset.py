from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import BaseUser
from ..serializers import UserRegisterSerializer


class UserRegisterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user registration.
    """
    queryset = BaseUser.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Handle user registration.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
