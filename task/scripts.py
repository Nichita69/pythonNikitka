import datetime
import random
from datetime import timedelta
from random import randint
from uuid import uuid4

from django.contrib.auth.models import User
from django.utils import timezone

from task.models import Task, Timer


def create_tasks():
    for x in range(25000):
        Task.objects.create(
            title=uuid4(),
            description=uuid4()
        )


def create_timers():
    for n in range(50000):
        Timer.objects.create(
            started_at=timezone.now(),
            stopped_at=timezone.now() + timedelta(minutes=randint(1, 10)),
            duration=timedelta(minutes=randint(1, 10)),
            task=Task.objects.all().order_by('?').first(),
            user=User.objects.all().order_by('?').first()
        )
