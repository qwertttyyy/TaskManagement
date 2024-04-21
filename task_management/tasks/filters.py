import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    """
    Фильтр для модели Task.
    Позволяет фильтровать задачи по статусу и дате создания.
    """

    status = django_filters.ChoiceFilter(
        field_name='status', choices=Task.STATUS_CHOICES
    )
    created_date = django_filters.DateTimeFilter(
        field_name='created_date', lookup_expr='date'
    )

    class Meta:
        model = Task
        fields = ['status', 'created_date']
