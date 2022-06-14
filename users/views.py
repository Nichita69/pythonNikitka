from django.contrib.auth.models import User
from django.db.models import Sum
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import datetime

from users.serializers import UserSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(UserSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            is_superuser=True,
            is_staff=True
        )
        user.set_password(validated_data['password'])
        user.save()

        return Response(UserSerializer(user).data)


class UsersListView(ListAPIView, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class UsersItemView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
    queryset = User.objects.all()

    def get(self, request, pk):
        user = self.get_object()
        today = datetime.datetime.now().date()
        start = today.replace(day=1)
        timelogs = user.timer_set.filter(
            started_at__gte=start,
            started_at__lte=today
        ).aggregate(Sum('duration'))
        return Response(timelogs)
