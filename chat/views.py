from itertools import zip_longest
from random import randrange

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from chat.models import rooms



class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        acs = rooms().filter(anonymous=True)
        cs = rooms().filter(anonymous=False)

        dictedrooms = [
            {'chatroom': c, 'anonchatroom': ac}
            for c, ac in zip_longest(cs, acs)
        ]

        context = {
            'rooms': dictedrooms
        }

        return render(request, 'chat/main.html', context=context)


def abstractroomview(anon: bool):
    class AbstractRoomView(View):

        def username(self, request: HttpRequest):
            return request.user.username

        def get(self, request: HttpRequest, room: str) -> HttpResponse:
            if not rooms().filter(url=room, anonymous=anon).exists():
                raise Http404('room with this name does not exist')

            context = {
                'room_name': room,
                'user_name': self.username(request),
                'anon': 'anon' if anon else '',
            }

            return render(request, 'chat/room.html', context=context)

    return AbstractRoomView


class AnonRoomView(abstractroomview(anon=True)):

    def get_anon_username(self, session):
        username = 'username'

        if username not in session:
            anon_id = str(randrange(0, 9999)).zfill(4)
            session[username] = f'anon#{anon_id}'

        return session[username]

    def username(self, request: HttpRequest):

        # print(request.session['username'])

        if request.user.is_anonymous:
            return self.get_anon_username(request.session)
        else:
            return super().username(request)


class RoomView(LoginRequiredMixin, abstractroomview(anon=False)):
    pass
