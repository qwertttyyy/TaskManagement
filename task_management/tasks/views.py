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
    queryset = Task.objects.select_related('user')
    serializer_class = TaskSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
