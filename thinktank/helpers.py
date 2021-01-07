import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http import JsonResponse
from django.views import View

from user.models import User


class AjaxView(LoginRequiredMixin, View):

    class RequestException(Exception):
        pass

    def okay_response(self, user: User, pk: int, **kwargs):
        return JsonResponse({'response': 'okay'} | kwargs)

    def error_response(self):
        return JsonResponse({'response': 'error'})

    def update_db(self, user: User, pk: int):
        return NotImplemented

    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body)
        pk = data['pk']
        user = request.user

        if data['type'] == 'fetch':
            return self.okay_response(user, pk)

        elif data['type'] == 'update':
            if user.is_anonymous:
                return self.error_response()
            else:
                self.update_db(user, pk)
                return self.okay_response(user, pk)

        else:
            raise AjaxView.RequestException('Bad ajax request type')


