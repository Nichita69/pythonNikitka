from datetime import timezone, datetime, timedelta

from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.db.models import Sum

from ruamel.yaml import comments

import task
import users

from django.urls import reverse
from django.test import TestCase
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from task.models import Task, Comment, Timer


class UsersApiTestCAse(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username='nichita', email='nichita@gmail.com', password='admin')
        token = self.client.post(path='/users/token/', data={
            "username": self.user.username,
            "password": "admin"
        }).json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    def test_retrieve_user(self):
        user = User.objects.create()
        response = self.client.get(f'/users/users/{user.id}/')
        self.assertEqual(HTTP_200_OK, response.status_code)
