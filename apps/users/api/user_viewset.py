from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions import IsAdmin
from ..models import BaseUser
from ..serializers import UserListSerializer, UserCreateStaffSerializer, UserRegisterSerializer, UserLogoutSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    ViewSet for listing users.
    """
    queryset = BaseUser.objects.all()
    serializer_class = UserListSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Assign permissions based on the action.
        """

        if self.action == 'staff':
            self.permission_classes = [IsAdmin]
        elif self.action == 'register':
            self.permission_classes = []
        return super().get_permissions()

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        # validate due to endpoints
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'me':
            return UserListSerializer
        elif self.action == 'staff':
            return UserCreateStaffSerializer
        elif self.action == 'register':
            return UserRegisterSerializer
        elif self.action == 'logout':
            return UserLogoutSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        """
        Handle GET requests to list users.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """
        Handle GET requests to retrieve the current user's information.
        """
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='staff')
    def staff(self, request):
        """
        Handle GET requests to retrieve the list of staff users.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """
        Handle POST requests to register a new user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """
        Handle POST requests to log out the current user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
