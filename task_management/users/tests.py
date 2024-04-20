from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CustomUser


class UserTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'Ivan',
            'email': 'ivan@example.com',
            'password': 'ivan1970',
        }

    def test_user_registration(self):
        response = self.client.post(reverse('register'), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertCountEqual(
            response.data.keys(), ['id', 'first_name', 'email']
        )
        self.assertIsInstance(response.data['id'], int)
        self.assertIsInstance(response.data['first_name'], str)
        self.assertIsInstance(response.data['email'], str)

        self.assertEqual(
            response.data['first_name'], self.user_data['first_name']
        )
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_user_registration_existing_email(self):
        CustomUser.objects.create_user(**self.user_data)
        response = self.client.post(reverse('register'), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['email'][0],
            'user with this email address already exists.',
        )
