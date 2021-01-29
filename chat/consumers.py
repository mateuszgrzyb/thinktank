import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import rooms


# noinspection PyAttributeOutsideInit
from user.models import priv_rooms
from user.models import PrivRoom


class AbstractChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f'{self.__class__.__name__}\'s constructor called.')

    history = {}

    async def send(self, text_data=None, bytes_data=None, close=False):
        print(text_data)
        await super().send(text_data, bytes_data, close)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        for msg in type(self).history[self.room_name]:
            await self.send(text_data=json.dumps(msg))

    async def disconnect(self, code):
        print('disconnect')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        msg = json.loads(text_data) | {'type': 'chat_msg'}

        type(self).history[self.room_name].append(msg)

        await self.channel_layer.group_send(
            self.room_group_name,
            msg
        )

    async def chat_msg(self, event):
        msg = {k: event[k] for k in event if k != 'type'}
        await self.send(text_data=json.dumps(msg))


# def historydecorator(allrooms):
#     def wrapped(clazz: type):
#         clazz.history = {room.url: [] for room in allrooms}
#         return clazz
#
#     return wrapped


class LoggedChatConsumer(AbstractChatConsumer):
    async def connect(self):
        print(self.scope['user'])
        print(self.scope['user'].is_anonymous)
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await super().connect()

    async def disconnect(self, code):
        try:
            await super().disconnect(code)
        except Exception:
            pass


class ChatConsumer(LoggedChatConsumer):
    history = {room.url: [] for room in rooms().filter(anonymous=False)}


class AnonChatConsumer(AbstractChatConsumer):
    history = {room.url: [] for room in rooms().filter(anonymous=True)}


#@historydecorator(priv_rooms())
class PrivChatConsumer(LoggedChatConsumer):
    pass
#    async def connect(self):
#        await super().connect()
#        room = PrivRoom.objects.filter(url=self.room_name).first()
#        if room is None or room.can_be_entered_by(self.scope['user']):
#            await self.close()
#