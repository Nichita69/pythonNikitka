from datetime import timezone, datetime, timedelta

from django.conf.global_settings import EMAIL_HOST_USER
from django.db.models import Sum
from ruamel.yaml import comments

import task
import users
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from task.models import Task, Comment, Timer


class TasksApiTestCAse(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username='nichita', email='nichita@gmail.com', password='admin')
        token = self.client.post(path='/users/token/', data={
            "username": self.user.username,
            "password": "admin"
        }).json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_task_list(self):
        response = self.client.get('/task/task/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_retrieve_task(self):
        task = Task.objects.create(description='Test', title='Test', user=self.user)
        response = self.client.get(f'/task/task/{task.id}/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_post_task_create(self):
        data = {
            "title": "Noroc",
            "description": "How are you"
        }
        response = self.client.post(f'/task/task/', data=data)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_task_update(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        data = {
            "title": "sgfdfg",
            "description": "bggfbfg",

        }
        response = self.client.put(f'/task/task/{task.id}/', data=data)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test__task_partial_update(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        data = {
            "title": "sgfdfg",
            "description": "bggfbfg",
        }
        response = self.client.patch(f'/task/task/{task.id}/', data=data)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_retrieve_task_delete(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        response = self.client.delete(f'/task/task/{task.id}/')
        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)

    def test_retrieve_comments(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        comment = Comment.objects.create(text='Test', user=self.user, task=task)
        response = self.client.get(f'/task/comments/{comment.id}/', task=task)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_post_comments_create(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        data = {
            "text": "Noroc",
            "task": task.id

        }
        response = self.client.post(f'/task/comments/', data=data)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_get_comments_list(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        response = self.client.get('/task/comments/', task=task)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_comments_partial_update(self):
        task = Task.objects.create(title='Test', user=self.user, description='Test')
        comment = Comment.objects.create(text='Test', user=self.user, task=task)
        data = {
            "text": "sgfdsdfg",
            "task": task.id
        }
        response = self.client.patch(f'/task/comments/{comment.id}/', data=data)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_comments_update(self):
        task = Task.objects.create(title='Test', user=self.user, description='Test')
        comment = Comment.objects.create(text='Test', user=self.user, task=task)
        data = {
            "text": "sghgfdsdfg",
            "task": task.id

        }
        response = self.client.put(f'/task/comments/{comment.id}/', data=data)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_comments_delete(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        comment = Comment.objects.create(text='Test', user=self.user, task=task)
        response = self.client.delete(f'/task/comments/{comment.id}/')
        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)

    def test_get_completed_tasks(self):
        response = self.client.get(f'/task/task/completed-tasks/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_get__list_time(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        timer = Timer.objects.create(started_at=timezone.now(), stopped_at=timezone.now(), task=task,
                                     user=self.user, is_stopped='True', is_running='True')

        response = self.client.get(f'/task/task/list_time/', timer=timer)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_get__my_tasks(self):
        response = self.client.get('/task/task/my-tasks/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_assign_task_to_user(self):
        task = Task.objects.create(title='Test', is_completed='False', user=self.user, description='Test')
        response = self.client.patch(f'/task/task/{task.id}/assign-task-to-user/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_task_complete(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        comment = Comment.objects.create(text='Test', user=self.user, task=task)
        response = self.client.patch(f'/task/task/{task.id}/complete/',comment=comment)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_get_list_log(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        response = self.client.get(f'/task/task/{task.id}/list_log/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_start_timer(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        response = self.client.post(f'/task/task/{task.id}/start_timer/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_stop_timer(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        timer = Timer.objects.create(started_at=timezone.now(), stopped_at=timezone.now(), task=task,
                                     user=self.user, is_stopped='True', is_running='True')

        response = self.client.post(f'/task/task/{task.id}/stop_timer/', timer=timer)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_get_task_comments(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        response = self.client.get(f'/task/task/{task.id}/task_comments/')
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_start_time_log(self):
        task = Task.objects.create(title='Test', is_completed='True', user=self.user, description='Test')
        timer = Timer.objects.create(started_at=timezone.now(), stopped_at=timezone.now(), task=task,
                                     user=self.user, is_stopped='True', is_running='True')
        data = {
            "started_at": timezone.now(),
            "duration": 6456

        }

        response = self.client.post(f'/task/task/{task.id}/time_log/', timer=timer, data=data)
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_retrieve_user(self):
        user = User.objects.create()
        response = self.client.get(f'/users/users/{user.id}/')
        self.assertEqual(HTTP_200_OK, response.status_code)

