from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    OpenApiExample,
)


def get_unique_id_param(name):
    return OpenApiParameter(
        name='id',
        description=f'Уникальный идентификатор {name}',
        required=True,
        location=OpenApiParameter.PATH,
    )


task_schema = {
    'list': extend_schema(
        summary='Получение всех задач',
        description='Возвращает список всех задач.',
        examples=[
            OpenApiExample(
                'list_tasks_example',
                summary='Пример ответа на получение всех задач',
                value=[
                    {
                        "id": 1,
                        "title": "Задача 1",
                        "description": "Описание задачи 1",
                        "status": "new",
                        "created_date": "2023-01-01T00:00:00Z",
                        "last_updated_date": "2023-01-01T00:00:00Z",
                        "user": {
                            "id": 1,
                            "first_name": "Иван",
                            "email": "ivan@example.com",
                        },
                    },
                    {
                        "id": 2,
                        "title": "Задача 2",
                        "description": "Описание задачи 2",
                        "status": "in_progress",
                        "created_date": "2023-01-02T00:00:00Z",
                        "last_updated_date": "2023-01-02T00:00:00Z",
                        "user": {
                            "id": 2,
                            "first_name": "Петр",
                            "email": "petr@example.com",
                        },
                    },
                ],
                response_only=True,
            )
        ],
        parameters=[
            OpenApiParameter(
                name='status',
                description='Фильтр по статусу задачи',
                required=False,
                type=str,
                enum=['new', 'in_progress', 'done'],
            ),
            OpenApiParameter(
                name='created_date',
                description='Фильтр по дате создания задачи',
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        'created_date_example',
                        summary='Пример значения для created_date',
                        value='2024-03-21',
                        request_only=True,
                    ),
                ],
            ),
        ],
    ),
    'retrieve': extend_schema(
        summary='Получение конкретной задачи',
        description='Возвращает задачу по переданному ID в параметре пути.',
        examples=[
            OpenApiExample(
                'retrieve_task_example',
                summary='Пример ответа на получение конкретной задачи',
                value={
                    "id": 1,
                    "title": "Задача 1",
                    "description": "Описание задачи 1",
                    "status": "new",
                    "created_date": "2023-01-01T00:00:00Z",
                    "last_updated_date": "2023-01-01T00:00:00Z",
                    "user": {
                        "id": 1,
                        "first_name": "Иван",
                        "email": "ivan@example.com",
                    },
                },
                response_only=True,
            )
        ],
        parameters=[get_unique_id_param('задачи')],
    ),
    'create': extend_schema(
        summary='Создание задачи',
        description='Создает новую задачу с данными, предоставленными в запросе.',
        examples=[
            OpenApiExample(
                'create_task_example',
                summary='Пример запроса на создание задачи',
                value={
                    "title": "Новая задача",
                    "description": "Описание новой задачи",
                    "status": "new",
                },
                request_only=True,
            ),
            OpenApiExample(
                'create_task_example',
                summary='Пример ответа на создание задачи',
                value={
                    "id": 3,
                    "title": "Новая задача",
                    "description": "Описание новой задачи",
                    "status": "new",
                    "created_date": "2023-01-03T00:00:00Z",
                    "last_updated_date": "2023-01-03T00:00:00Z",
                    "user": {
                        "id": 1,
                        "first_name": "Иван",
                        "email": "ivan@example.com",
                    },
                },
                response_only=True,
            ),
        ],
    ),
    'partial_update': extend_schema(
        summary='Частичное обновление задачи',
        description='Обновляет часть данных задачи с указанным ID.',
        examples=[
            OpenApiExample(
                'patch_task_example',
                summary='Пример запроса на частичное обновление задачи',
                value={"status": "in_progress"},
                request_only=True,
            ),
            OpenApiExample(
                'patch_task_example',
                summary='Пример ответа на частичное обновление задачи',
                value={
                    "id": 1,
                    "title": "Задача 1",
                    "description": "Описание задачи 1",
                    "status": "in_progress",
                    "created_date": "2023-01-01T00:00:00Z",
                    "last_updated_date": "2023-01-03T00:00:00Z",
                    "user": {
                        "id": 1,
                        "first_name": "Иван",
                        "email": "ivan@example.com",
                    },
                },
                response_only=True,
            ),
        ],
        parameters=[get_unique_id_param('задачи')],
    ),
    'destroy': extend_schema(
        summary='Удаление задачи',
        description='Удаляет задачу с указанным ID.',
        parameters=[get_unique_id_param('задачи')],
    ),
}
