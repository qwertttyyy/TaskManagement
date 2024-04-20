from rest_framework import viewsets

from .models import Task
from .permissions import OwnerOrReadOnly
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('user')
    serializer_class = TaskSerializer
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
