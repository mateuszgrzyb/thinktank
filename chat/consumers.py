import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import rooms


# noinspection PyAttributeOutsideInit
class AbstractChatConsumer(AsyncWebsocketConsumer):
    history = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        for msg in self.history[self.room_name]:
            await self.send(text_data=json.dumps(msg))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        msg = json.loads(text_data) | {'type': 'chat_msg'}

        await self.channel_layer.group_send(
            self.room_group_name,
            msg
        )

    async def chat_msg(self, event):
        msg = {k: event[k] for k in event if k != 'type'}
        self.history[self.room_name].append(msg)
        await self.send(text_data=json.dumps(msg))


def historydecorator(anonymous: bool):
    def wrapped(clazz: type):
        clazz.history = {room.url: [] for room in rooms().filter(anonymous=anonymous)}
        return clazz

    return wrapped


@historydecorator(anonymous=False)
class ChatConsumer(AbstractChatConsumer):

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



@historydecorator(anonymous=True)
class AnonChatConsumer(AbstractChatConsumer):
    pass
