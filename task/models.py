# Create your models here.
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django_filters import fields


class Task(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_completed = models.BooleanField(default=False)


class Comment(models.Model):
    text = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Timer(models.Model):
    started_at = models.DateTimeField(null=True, blank=True)
    stopped_at = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(default=timedelta())
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_stopped = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)

