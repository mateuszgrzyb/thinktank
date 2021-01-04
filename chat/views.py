from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, redirect
from django.views import View

from chat.models import rooms


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        username = 'anon' if (u := request.user).is_anonymous else u.username

        context = {
            'rooms': rooms().all(),
            'username': username,
        }

        return render(request, 'main.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        if (data := request.POST['room'].split(':'))[0] == 'True':
            return redirect('anon', room=data[1])
        elif data[0] == 'False':
            return redirect('room', room=data[1])
        else:
            raise Exception("bruh what the fuck?")


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
    ANID = 0

    def username(self, request: HttpRequest):
        if request.user.is_anonymous:
            return f'anon#{str(self.ANID).zfill(4)}'
        else:
            return super().username(request)


class RoomView(LoginRequiredMixin, abstractroomview(anon=False)):
    pass
