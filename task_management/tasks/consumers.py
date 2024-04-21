import json

from channels.generic.websocket import AsyncWebsocketConsumer


GROUP_NAME = 'notifications'


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Класс для обработки веб-сокет соединений и отправки уведомлений.
    Подключается к группе при подключении и отключается при отключении.
    Отправляет уведомления, полученные от группы, клиенту.
    """

    async def connect(self):
        self.group_name = GROUP_NAME
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))
