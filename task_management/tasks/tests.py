from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
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
            'password': 'petr1980',
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.other_user = CustomUser.objects.create_user(
            **self.other_user_data
        )
        self.client.force_authenticate(user=self.user)

        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Task Description',
        }
        self.other_task_data = {
            'title': ' Second Test Task',
            'description': 'Other Test Task Description',
            'status': 'in_progress',
        }
        self.task = Task.objects.create(user=self.user, **self.task_data)
        self.other_task = Task.objects.create(
            user=self.user, **self.other_task_data
        )

        self.task_list_url = reverse('task-list')
        self.task_detail_url = reverse(
            'task-detail', kwargs={'pk': self.task.pk}
        )

    def check_task_response(self, response, task_data):
        """Функция для проверки ответа на операции с задачами.
        Проверяем, что статус код ответа равен 200 OK или 201 CREATED.
        Проверяем, что в ответе есть поля 'title', 'description', 'status'
        и они совпадают с переданными данными."""

        self.assertIn(
            response.status_code, (status.HTTP_200_OK, status.HTTP_201_CREATED)
        )
        self.assertEqual(response.data['title'], task_data['title'])
        self.assertEqual(
            response.data['description'], task_data['description']
        )
        self.assertEqual(response.data['status'], 'new')

    def test_create_task(self):
        """
        Тест создания задачи.
        Ожидаемый результат: создание задачи с кодом 201 CREATED и проверка
        ответа с помощью check_task_response.
        """
        response = self.client.post(self.task_list_url, data=self.task_data)
        self.check_task_response(response, self.task_data)

    def test_get_task_detail(self):
        """
        Тест получения деталей задачи.
        Ожидаемый результат: получение деталей задачи с кодом 200 OK и проверка
        ответа с помощью check_task_response.
        """
        response = self.client.get(self.task_detail_url)
        self.check_task_response(response, self.task_data)

    def test_get_task_list(self):
        """
        Тест получения списка задач.
        Ожидаемый результат: получение списка задач с кодом 200 OK и проверка,
        что в списке есть одна задача.
        """
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_task(self):
        """
        Тест обновления задачи.
        Ожидаемый результат: обновление задачи с кодом 200 OK и проверка,
        что поле 'status' было обновлено.
        """
        new_data = {'status': 'in_progress'}
        response = self.client.patch(self.task_detail_url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], new_data['status'])

    def test_delete_task(self):
        """
        Тест удаления задачи.
        Ожидаемый результат: удаление задачи с кодом 204 NO CONTENT.
        """
        response = self.client.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_task_not_authenticated(self):
        """
        Тест создания задачи неавторизованным пользователем.
        Ожидаемый результат: возвращается код 401 UNAUTHORIZED.
        """
        self.client.logout()
        response = self.client.post(reverse('task-list'), data=self.task_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_other_users_task(self):
        """
        Тест попытки обновления не своей задачи.
        Ожидаемый результат: возвращается код 403 FORBIDDEN.
        """

        other_users_task = Task.objects.create(
            user=self.other_user, **self.task_data
        )
        new_data = {'status': 'in_progress'}
        response = self.client.patch(
            reverse('task-detail', kwargs={'pk': other_users_task.pk}),
            data=new_data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_date(self):
        """
        Тест на фильтрацию по дате.
        Ожидаемый результат: Каждая задача в ответе имеет переданную дату.
        """

        self.other_task.created_date -= timedelta(days=1)
        self.other_task.save()
        now_date = f'{timezone.now():%Y-%m-%d}'
        response = self.client.get(
            self.task_list_url, {'created_date': now_date}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for task in response.data:
            with self.subTest(task=task):
                self.assertIn(now_date, task['created_date'])

    def test_filter_by_status(self):
        """
        Тест на фильтрацию по статусу.
        Ожидаемый результат: Каждая задача в ответе имеет переданный статус.
        """

        response = self.client.get(self.task_list_url, {'status': 'new'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for task in response.data:
            with self.subTest(task=task):
                self.assertEqual(task['status'], 'new')
