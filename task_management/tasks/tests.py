from datetime import timedelta

from django.core.cache import cache
from django.forms import model_to_dict
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import CustomUser

from .models import Task


class TaskTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1_data = {
            'first_name': 'Ivan',
            'email': 'ivan@example.com',
            'password': 'ivan1970',
        }
        cls.user_2_data = {
            'first_name': 'Petr',
            'email': 'petr@example.com',
            'password': 'petr1980',
        }
        cls.user_1 = CustomUser.objects.create_user(**cls.user_1_data)
        cls.user_2 = CustomUser.objects.create_user(**cls.user_2_data)

        cls.user_1_task_data = {
            'title': 'Test Task',
            'description': 'Test Task Description',
        }
        cls.user_2_task_data = {
            'title': ' Second Test Task',
            'description': 'Other Test Task Description',
            'status': 'in_progress',
        }
        cls.task_user_1 = Task.objects.create(
            user=cls.user_1, **cls.user_1_task_data
        )
        cls.task_user_2 = Task.objects.create(
            user=cls.user_2, **cls.user_2_task_data
        )

        cls.task_list_url = reverse('task-list')
        cls.task_user_1_detail_url = reverse(
            'task-detail', kwargs={'pk': cls.task_user_1.pk}
        )

    def setUp(self):
        cache.clear()
        self.client_user_1 = APIClient()
        self.client_user_1.force_authenticate(user=self.user_1)

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

        response = self.client_user_1.post(
            self.task_list_url, data=self.user_1_task_data
        )
        self.check_task_response(response, self.user_1_task_data)

    def test_get_task_detail(self):
        """
        Тест получения деталей задачи.
        Ожидаемый результат: получение деталей задачи с кодом 200 OK и проверка
        ответа с помощью check_task_response.
        """

        response = self.client.get(self.task_user_1_detail_url)
        self.check_task_response(response, self.user_1_task_data)

    def test_get_task_list(self):
        """
        Тест получения списка задач.
        Ожидаемый результат: получение списка задач с кодом 200 OK и проверка,
        что в списке ожидаемое количество задач.
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
        response = self.client_user_1.patch(
            self.task_user_1_detail_url, data=new_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], new_data['status'])

    def test_delete_task(self):
        """
        Тест удаления задачи.
        Ожидаемый результат: удаление задачи с кодом 204 NO CONTENT.
        """

        response = self.client_user_1.delete(self.task_user_1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_task_not_authenticated(self):
        """
        Тест создания задачи неавторизованным пользователем.
        Ожидаемый результат: возвращается код 401 UNAUTHORIZED.
        """

        response = self.client.post(
            reverse('task-list'), data=self.user_1_task_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_other_users_task(self):
        """
        Тест попытки обновления не своей задачи.
        Ожидаемый результат: возвращается код 403 FORBIDDEN.
        """

        new_data = {'status': 'in_progress'}
        response = self.client_user_1.patch(
            reverse('task-detail', kwargs={'pk': self.task_user_2.pk}),
            data=new_data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_date(self):
        """
        Тест на фильтрацию по дате.
        Ожидаемый результат: Каждая задача в ответе имеет переданную дату.
        """

        self.task_user_2.created_date -= timedelta(days=1)
        self.task_user_2.save()
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

    def test_current_user_task_list(self):
        """
        Тест на получение списка задач авторизованного пользователя
        Ожидаемый результат: В списке задач только задачи
        пользователя сделавшего запрос
        """
        response = self.client_user_1.get(reverse('task-my-tasks'))
        for task in response.data:
            with self.subTest(task=task):
                self.assertEqual(
                    task['user'],
                    model_to_dict(
                        self.user_1,
                        fields=['id', 'email', 'first_name'],
                    ),
                )
