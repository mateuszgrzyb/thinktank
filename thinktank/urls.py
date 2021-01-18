import os

from django.contrib import admin
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.views import View
from markdown import markdown

from thinktank.mixins import AjaxView


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        with open('./README.md') as f:
            readme = markdown(f.read())
            context = {'readme': readme}
            return render(request, 'home.html', context=context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('chat/', include('chat.urls', namespace='chat')),
    path('user/', include('user.urls', namespace='user')),
    path('post/', include('post.urls', namespace='post')),
    path('ajax/', AjaxView.as_view(), name='ajax')
]
