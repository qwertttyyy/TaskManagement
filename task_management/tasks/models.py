from django.db import models

from users.models import CustomUser


class Task(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'В процессе'),
        ('done', 'Выполнена'),
    )

    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.CharField(max_length=300, verbose_name='Описание')
    status = models.CharField(
        verbose_name='Статус',
        max_length=20,
        default='new',
        choices=STATUS_CHOICES,
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
    last_updated_date = models.DateTimeField(
        default=None, null=True, verbose_name='Дата последнего обновления'
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks',
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ('-created_date',)

    def __str__(self):
        return f'Задача {self.title} пользователя {self.user.first_name}'
