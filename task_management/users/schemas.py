from drf_spectacular.utils import OpenApiExample

from .serializers import UserSerializer

user_registration_schema = {
    'summary': 'Регистрация нового пользователя',
    'description': 'Создает нового пользователя с данными, предоставленными в запросе.',
    'request': UserSerializer,
    'examples': [
        OpenApiExample(
            'create_user_example',
            summary='Пример запроса на регистрацию пользователя',
            value={
                "first_name": "Иван",
                "email": "ivan@example.com",
                "password": "securepassword123",
            },
            request_only=True,
        ),
        OpenApiExample(
            'create_user_example',
            summary='Пример ответа на регистрацию пользователя',
            value={
                "id": 1,
                "first_name": "Иван",
                "email": "ivan@example.com",
            },
            response_only=True,
        ),
    ],
}
