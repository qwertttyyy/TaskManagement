from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    queryset = Task.objects.select_related('user')
    serializer_class = TaskSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache.clear()

    def perform_update(self, serializer):
        serializer.save()
        cache.clear()

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()

    @method_decorator(cache_page(60 * 60))
    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
        url_path='my-tasks',
        url_name='my-tasks',
        filter_backends=(DjangoFilterBackend,),
        filterset_class=TaskFilter,
    )
    def current_user_tasks(self, request):
        filtered_queryset = self.filter_queryset(self.queryset)
        user_tasks = filtered_queryset.filter(user=request.user)
        serializer = self.get_serializer(user_tasks, many=True)
        return Response(serializer.data)
