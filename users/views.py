from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.serializers import UserSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()


class UsersListView(ListAPIView, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class UsersItemView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
    queryset = User.objects.all()
