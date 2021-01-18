import json
from abc import abstractmethod

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import reverse
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
            pk=data.get('id'),
        )

        return HttpResponse(status=200)


class BackSuccessUrlNextPageMixin:
    def get_back_url(self):
        return reverse('home')

    def get_next_page(self):
        return self.get_back_url()

    def get_success_url(self):
        return self.get_back_url()
