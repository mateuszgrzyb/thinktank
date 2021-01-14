from django.urls import re_path

from chat.consumers import ChatConsumer, AnonChatConsumer
from chat.consumers import PrivChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/anonchat/(?P<room_name>\w+)/$', AnonChatConsumer.as_asgi()),
    re_path(r'ws/privchat/(?P<user_name>\w+)/$', PrivChatConsumer.as_asgi()),
]
