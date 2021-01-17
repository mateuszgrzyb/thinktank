import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http import HttpResponse
from django.views import View

from thinktank.helpers import back_url


class AjaxView(LoginRequiredMixin, View):
    switch = {
        'like': lambda **kwargs: kwargs['user'].click_like(post_pk=kwargs['pk']),
        'follow': lambda **kwargs: kwargs['user'].click_follow(user_pk=kwargs['pk']),
    }

    def post(self, request: HttpRequest) -> HttpResponse:
        data = json.loads(request.body)

        self.switch[data['request']](
            user=request.user,
            pk=data['id']
        )

        return HttpResponse(status=200)


class BackSuccessUrlMixin:
    def get_success_url(self):
        return back_url(self.request)
