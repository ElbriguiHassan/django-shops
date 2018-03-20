from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.conf import settings

from permissions import (
    UserObjectOwnerPermission,
    UserPermission
)
from serializers import (
    UserSerializer, PasswordSerializer
)
from app_settings import app_settings


User = get_user_model()


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """ Users
    This endpoint used by anonymous users on POST to create/register new users.
    """
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all().exclude(status=app_settings.STATUS_DELETED)
    permission_classes = (UserPermission, UserObjectOwnerPermission)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'current':
            return self.request.user

        return super(UserViewSet, self).get_object()

    def update(self, request, *args, **kwargs):
        # Allow partials for updating single values
        kwargs.update(
            dict(
                partial=True
            )
        )
        return super(UserViewSet, self).update(request, *args, **kwargs)

    @detail_route(methods=['patch', 'put'], permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)