from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r"ws/private-chat-server", consumers.PrivateChatConsumer.as_asgi())
]