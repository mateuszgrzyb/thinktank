from itertools import zip_longest
from random import randrange

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from chat.models import rooms
from user.models import User


class GroupChatSelectionView(TemplateView):
    template_name = 'chat/main.html'
    extra_context = {
        'rooms': [{
            'chatroom': c,
            'anonchatroom': ac
        } for c, ac in zip_longest(
            rooms().filter(anonymous=True),
            rooms().filter(anonymous=False),
        )]}


# def abstractroomview(anon: bool):
#     class AbstractRoomView_(View):
#
#         def username(self, request: HttpRequest):
#             return request.user.username
#
#         def get(self, request: HttpRequest, room: str) -> HttpResponse:
#             if not rooms().filter(url=room, anonymous=anon).exists():
#                 raise Http404('room with this name does not exist')
#
#             context = {
#                 'room_name': room,
#                 'user_name': self.username(request),
#                 'anon': 'anon' if anon else '',
#             }
#
#             return render(request, 'chat/room.html', context=context)
#
#     return AbstractRoomView_


class BaseRoomView(TemplateView):
    template_name = 'chat/room.html'
    room_type = ''

    def get_username(self):
        return self.request.user.username

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            'room_name': self.kwargs['room'],
            'user_name': self.get_username(),
            'type': type(self).room_type,
        }


class AnonRoomView(BaseRoomView):
    room_type = 'anon'

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
    pass


class PrivChatSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/privchatselection.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            'convos': self.request.user.all_priv_rooms()
        }


# class PrivChatView(LoginRequiredMixin, TemplateView):
#     template_name = 'chat/privchat.html'

class PrivChatView(LoginRequiredMixin, BaseRoomView):
    room_type = 'priv'
