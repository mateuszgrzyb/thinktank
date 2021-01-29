import json

import bleach as bleach
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from markdown import markdown


def get_readme(filename: str):
    with open('./README.md') as f:
        return markdown(f.read())


class AjaxView(LoginRequiredMixin, View):
    switch = {
        'like': lambda **kwargs: kwargs['user'].click_like(post_pk=kwargs['pk']),
        'follow': lambda **kwargs: kwargs['user'].click_follow(user_pk=kwargs['pk']),
    }

    def post(self, request: HttpRequest) -> HttpResponse:
        data = json.loads(request.body)

        self.switch[data['request']](
            user=request.user,
            pk=data.get('pk'),
        )

        return HttpResponse(status=200)


class HomeView(TemplateView):
    extra_context = {'readme': get_readme('./README.md')}
    template_name = 'home.html'
