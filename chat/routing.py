from django.urls import path
from django.urls import re_path

from chat.consumers import ChatConsumer, AnonChatConsumer
from chat.consumers import PrivChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/anonchat/(?P<room_name>\w+)/$', AnonChatConsumer.as_asgi()),
    # re_path(r'ws/privchat/(?P<room_name>\w+)/$', PrivChatConsumer.as_asgi()),
    re_path(
        r'ws/privchat/(?P<room_name>[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12})/$',
        PrivChatConsumer.as_asgi()
    ),
]
