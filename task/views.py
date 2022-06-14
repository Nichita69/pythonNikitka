import datetime
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.settings import EMAIL_HOST_USER
from task.models import Task, Comment, Timer
from task.serializers import TaskSerializer, CreateTaskSerializer, AssignTaskToUser, ListTaskSerializer, \
    CommentSerializer, CreateCommentSerializer, TimerSerializer, CreateTimerSerializer, ListTimerLogSerializer, \
    TaskTimeSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCommentSerializer
        else:
            return super(CommentViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data)


class TaskViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTaskSerializer
        elif self.action == "list":
            return ListTaskSerializer
        else:
            return super(TaskViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = serializer.save(user=request.user)
        user = task.user
        user.email_user(
            subject='Transmiterea taskului',
            message='Am transmis acest task si gasesc useru dupa aidi',
            from_email=EMAIL_HOST_USER
        )

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my-tasks')
    def my_tasks(self, request, *args, **kwargs):
        user = request.user
        tasks = Task.objects.filter(user=user)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(detail=False, methods=['get'], url_path='completed-tasks')
    def completed_tasks(self, request, *args, **kwargs):
        tasks = Task.objects.filter(is_completed=True)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(detail=True, methods=['patch'], serializer_class=AssignTaskToUser, url_path='assign-task-to-user')
    def assign_task_to_user(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.update(task, serializer.validated_data)
        task.user.email_user(
            subject='Adaugarea tasc',
            message='Dali znacenii taska useru,i otpravili soobsenie na postu ',
            from_email=EMAIL_HOST_USER
        )
        return Response(TaskSerializer(task).data)

    @action(detail=True, methods=['patch'], serializer_class=Serializer, url_path='complete')
    def complete(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_completed = True
        task.save()
        users = User.objects.filter(comment__task_id=task.id).distinct()

        for user in users:
            user.email_user(
                subject='Commented task',
                message='Am commentat acest task si am gasit coment task duoa id',
                from_email=EMAIL_HOST_USER
            )

        return Response(TaskSerializer(task).data)

    @action(detail=True, methods=['get'], serializer_class=Serializer, url_path="task_comments")
    def task_comments(self, request, *args, **kwargs):
        task = self.get_object()
        comments = Comment.objects.filter(task=task)
        return Response(CommentSerializer(comments, many=True).data)

    @action(detail=True, methods=['post'], serializer_class=Serializer, url_path="start_timer")
    def start_timer(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user
        timer = Timer.objects.create(
            started_at=timezone.now(),
            task=task,
            user=user,
            is_running=True

        )
        return Response(timer.id)

    @action(detail=True, methods=['post'], serializer_class=Serializer, url_path='stop_timer')
    def stop_timer(self, request, *args, **kwargs):
        task = self.get_object()
        timer = Timer.objects.filter(task_id=task.id).last()
        timer.stopped_at = timezone.now()
        timer.duration = timer.stopped_at - timer.started_at
        timer.is_stopped = True
        timer.is_running = False
        timer.save()
        return Response(timer.id)

    @action(detail=True, methods=['get'], serializer_class=ListTimerLogSerializer, url_path="list_log")
    def list_log(self, request, *args, **kwargs):

        task = self.get_object()
        timelogs = Timer.objects.filter(task=task)

        return Response(ListTimerLogSerializer(timelogs, many=True).data)

    @action(detail=True, methods=['post'], serializer_class=CreateTimerSerializer, url_path="time_log")
    def time_log(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        timer = serializer.save(
            user=request.user,
            task=task,
            stopped_at=validated_data["started_at"] + validated_data["duration"],
            is_stopped=True,

        )
        return Response(TimerSerializer(timer).data)

    @cache_page(60 * 15)
    @action(detail=False, methods=['get'], serializer_class=TaskTimeSerializer, url_path="list_time")
    def list_time(self, request, *args, **kwargs):
        today = timezone.now()
        start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        task = self.get_queryset().prefetch_related(
            'timer_set',
        ).filter(
            timer__started_at__gte=start,
            timer__started_at__lte=today
        )[:20].annotate(duration=Sum('timer__duration'))
        return Response(TaskTimeSerializer(task, many=True).data)
