from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser
from .models import Task


class TaskTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'Ivan',
            'email': 'ivan@example.com',
            'password': 'ivan1970',
        }
        self.other_user_data = {
            'first_name': 'Petr',
            'email': 'petr@example.com',
            'password': 'petr1970',
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.other_user = CustomUser.objects.create_user(
            **self.other_user_data
        )
        self.client.force_authenticate(user=self.user)
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Task Description',
            'status': 'new',
        }
        self.task = Task.objects.create(user=self.user, **self.task_data)
        self.task_list_url = reverse('task-list')
        self.task_detail_url = reverse(
            'task-detail', kwargs={'pk': self.task.pk}
        )

    def check_task_response(self, response, task_data):
        self.assertIn(
            response.status_code, (status.HTTP_200_OK, status.HTTP_201_CREATED)
        )
        self.assertEqual(response.data['title'], task_data['title'])
        self.assertEqual(
            response.data['description'], task_data['description']
        )
        self.assertEqual(response.data['status'], task_data['status'])

    def test_create_task(self):
        response = self.client.post(self.task_list_url, data=self.task_data)
        self.check_task_response(response, self.task_data)

    def test_get_task_detail(self):
        response = self.client.get(self.task_detail_url)
        self.check_task_response(response, self.task_data)

    def test_get_task_list(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_task(self):
        new_data = {'status': 'in_progress'}
        response = self.client.patch(self.task_detail_url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], new_data['status'])

    def test_delete_task(self):
        response = self.client.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_task_not_authenticated(self):
        self.client.logout()
        response = self.client.post(reverse('task-list'), data=self.task_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_other_users_task(self):
        other_users_task = Task.objects.create(
            user=self.other_user, **self.task_data
        )
        new_data = {'title': 'New Test Task'}
        response = self.client.patch(
            reverse('task-detail', kwargs={'pk': other_users_task.pk}),
            data=new_data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
