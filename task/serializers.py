from task.models import Task, Comment, Timer
from rest_framework import serializers
from datetime import datetime, timedelta


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "user", "is_completed")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text", "id", "user", "task")


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description")


class ListTaskSerializer(serializers.ModelSerializer):
    total_duration = serializers.SerializerMethodField()

    def get_total_duration(self, obj):
        from django.db.models import Avg, Count, Min, Sum
        timelogs = Timer.objects.filter(task=obj).aggregate(sumofsecond=Sum('duration'))

        return timelogs['sumofsecond']

    class Meta:
        model = Task
        fields = ("id", "title", "total_duration")


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("task", "text")


class AssignTaskToUser(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("user",)


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = ("id",)


class CreateTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = ("started_at", "duration")


class ListTimerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = "__all__"


class TaskTimeSerializer(serializers.ModelSerializer):
    duration = serializers.DurationField(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
