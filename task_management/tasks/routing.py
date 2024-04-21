from django.urls import path

from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path('api/ws/notification/', NotificationConsumer.as_asgi()),
]
