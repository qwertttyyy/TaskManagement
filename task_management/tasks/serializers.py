from django.utils import timezone
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=Task.STATUS_CHOICES, required=False
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_date', 'user')

    def update(self, task, validated_data):
        for attr, value in validated_data.items():
            setattr(task, attr, value)
        task.last_updated_date = timezone.now()
        task.save()
        return task
