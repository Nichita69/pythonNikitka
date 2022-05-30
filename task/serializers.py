from task.models import Task, Comment
from rest_framework import serializers


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
    class Meta:
        model = Task
        fields = "__all__"


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("task", "text")


class AssignTaskToUser(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("user",)
