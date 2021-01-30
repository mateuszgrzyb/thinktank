import json
from collections import defaultdict

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

# # noinspection PyAttributeOutsideInit
# class AbstractChatConsumer(AsyncWebsocketConsumer):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         print(f'{self.__class__.__name__}\'s constructor called.')
#
#     history: dict[str, list[Any]]
#
#     # async def send(self, text_data=None, bytes_data=None, close=False):
#     #     print(text_data)
#     #     await super().send(text_data, bytes_data, close)
#
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f"chat_{self.room_name}"
#
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#         for msg in type(self).history[self.room_name]:
#             await self.send(text_data=json.dumps(msg))
#
#     async def disconnect(self, code):
#         print('disconnect')
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data=None, bytes_data=None):
#         msg = json.loads(text_data) | {'type': self.chat_msg.__name__}
#
#         type(self).history[self.room_name].append(msg)
#
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             msg
#         )
#
#     async def chat_msg(self, event):
#         msg = {k: event[k] for k in event if k != 'type'}
#         await self.send(text_data=json.dumps(msg))
from user.models import priv_rooms


class ChannelsWebsocketConsumer(AsyncWebsocketConsumer):
    url_parameter: str

    async def connect(self):
        self.name = self.scope['url_route']['kwargs'][type(self).url_parameter]
        self.group_name = f"chat_{self.name}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


# noinspection PyAttributeOutsideInit
class AbstractChatConsumer(ChannelsWebsocketConsumer):
    history: dict[str, list[dict]]
    url_parameter = 'room_name'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'type'

    async def connect(self):
        await super().connect()
        for msg in type(self).history[self.name]:
            await self.send(text_data=json.dumps(msg))

    async def receive(self, text_data=None, bytes_data=None):
        msg = json.loads(text_data) | {self.type: self.on_channel_receive.__name__}

        type(self).history[self.name].append(msg)

        await self.channel_layer.group_send(self.group_name, msg)

    async def on_channel_receive(self, event):
        msg = {k: event[k] for k in event if k != self.type}
        await self.send(text_data=json.dumps(msg))


class LoggedChatConsumer(AbstractChatConsumer):
    async def connect(self):
        print('connect')
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await super().connect()

    async def disconnect(self, code):
        try:
            await super().disconnect(code)
        except Exception:
            pass


from chat.models import rooms


class ChatConsumer(LoggedChatConsumer):
    history = {room.url: [] for room in rooms().filter(anonymous=False)}


class AnonChatConsumer(AbstractChatConsumer):
    history = {room.url: [] for room in rooms().filter(anonymous=True)}


class PrivChatConsumer(LoggedChatConsumer):
    history = {str(room.url): [] for room in priv_rooms()}

    @sync_to_async
    def can_enter(self):
        user = self.scope['user']
        room = priv_rooms().filter(url=self.name).first()
        return room is not None and room.can_be_entered_by(user)

    @sync_to_async
    def check_url(self):
        url = self.scope['url_route']['kwargs'][type(self).url_parameter]
        if url not in type(self).history:
            if not priv_rooms().filter(url=url).exists():
                return False
            else:
                type(self).history[url] = []
        return True

    async def connect(self):
        if await self.check_url():
            await super().connect()
            if not await self.can_enter():
                await self.close()
