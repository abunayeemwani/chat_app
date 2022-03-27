import imp
from django.urls import path
from main import consumers

websocket_urlpatterns = [
    path('', consumers.ChatConsumer.as_asgi()),
]