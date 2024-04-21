from django.utils import timezone
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Task
from .utils import send_task_status_change_notification


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для задач.
    Включает поля:
        название, описание, статус, автор, даты создания и обновления.
    """

    status = serializers.ChoiceField(
        choices=Task.STATUS_CHOICES, required=False
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_date',)

    def update(self, task, validated_data):
        """
        Переопределение метода обновления с изменением даты
        последнего обновления задачи.
        """

        for attr, value in validated_data.items():
            if attr == 'status' and task.status != value:
                send_task_status_change_notification(task, value)
            setattr(task, attr, value)
        task.last_updated_date = timezone.now()
        task.save()
        return task
