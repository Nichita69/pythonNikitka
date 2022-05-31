from django.contrib.auth.models import User
from rest_framework import serializers
from task.models import Timer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password",)


class CreateTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = ("started_at", "duration")


class ListTimerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = "__all__"
