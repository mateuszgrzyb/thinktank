from django.urls import re_path

from chat.consumers import ChatConsumer, AnonChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/anonchat/(?P<room_name>\w+)/$', AnonChatConsumer.as_asgi()),
]
