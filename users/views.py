from django.contrib.auth.models import User
from django.db.models import Sum
from drf_util.decorators import serialize_decorator
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import datetime

from task.models import Timer

from users.serializers import UserSerializer, ListTimerLogSerializer


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

    def get(self, request, pk):
        user = self.get_object()
        today = datetime.datetime.now().date()
        start = today.replace(day=1)
        timelogs = user.timer_set.filter(
            started_at__gte=start,
            started_at__lte=today
        ).aggregate(Sum('duration'))
        return Response(timelogs)

