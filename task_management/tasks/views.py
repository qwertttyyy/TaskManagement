from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets

from .filters import TaskFilter
from .models import Task
from .permissions import OwnerOrReadOnly
from .schemas import task_schema
from .serializers import TaskSerializer


@extend_schema(tags=['Задачи'])
@extend_schema_view(**task_schema)
class TaskViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с задачами.
    Создание, чтение, обновление и удаление задач.
    Фильтрация задач по статусу и дате создания.
    Кэширует список задач до момента их изменения.
    """

    serializer_class = TaskSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        tasks = cache.get('tasks')
        if not tasks:
            tasks = Task.objects.select_related('user')
            cache.set('tasks', tasks)
        return tasks

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache.delete('tasks')

    def perform_destroy(self, instance):
        instance.save()
        cache.delete('tasks')

    def perform_update(self, serializer):
        serializer.save()
        cache.delete('tasks')
