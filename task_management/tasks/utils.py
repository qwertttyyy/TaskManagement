from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_task_status_change_notification(task, new_status):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'public_room',
        {
            'type': 'send_notification',
            'message': f'Изменился статус задачи {task.title} '
            f'с {task.status} на {new_status}',
        },
    )
