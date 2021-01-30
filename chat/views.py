from abc import abstractmethod
from itertools import zip_longest
from random import randrange

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from chat.models import rooms
from user.models import User
from user.models import priv_rooms


class GroupChatSelectionView(TemplateView):
    template_name = 'chat/main.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data() | {
            'rooms': [{
                'chatroom': c,
                'anonchatroom': ac
            } for c, ac in zip_longest(
                rooms().filter(anonymous=True),
                rooms().filter(anonymous=False),
            )]
        }


class PrivChatSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/privchatselection.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            'convos': self.request.user.get_all_priv_rooms()
        }


class BaseRoomView(TemplateView):
    template_name = 'chat/room.html'
    room_type = ''

    @abstractmethod
    def get_room_name(self, url: str):
        pass

    def get_username(self):
        return self.request.user.username

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            'room_name': self.kwargs['room'],
            'user_name': self.get_username(),
            'type': type(self).room_type,
            'title': self.get_room_name(self.kwargs['room'])
        }


class AnonRoomView(BaseRoomView):
    room_type = 'anon'

    def get_room_name(self, url: str):
        return f'Anonymous {rooms().get(Q(url=url) & Q(anonymous=True)).name}'

    def get_anon_username(self):
        session = self.request.session
        username = 'username'

        if username not in session:
            anon_id = str(randrange(0, 9999)).zfill(4)
            session[username] = f'anon#{anon_id}'

        return session[username]

    def get_username(self):
        if self.request.user.is_anonymous:
            return self.get_anon_username()
        else:
            return super().get_username()


class RoomView(LoginRequiredMixin, BaseRoomView):
    def get_room_name(self, url: str):
        return f'{rooms().get(Q(url=url) & Q(anonymous=False)).name}'


# class PrivChatView(LoginRequiredMixin, TemplateView):
#     template_name = 'chat/privchat.html'

class PrivChatView(LoginRequiredMixin, BaseRoomView):
    room_type = 'priv'

    def get_room_name(self, url: str):
        user = self.request.user
        priv_room = priv_rooms().get(url=url)
        u1, u2 = priv_room.user1, priv_room.user2
        another_user = u1 if u2 == user else u2
        return {
            'name': 'Private Chat with',
            'pk': another_user.pk,
            'user': f'@{another_user.username}',
        }


