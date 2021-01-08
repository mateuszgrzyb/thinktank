import json
from abc import abstractmethod

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.http import Http404
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.views.generic import DetailView
from django.views.generic import ListView

from thinktank.models import AjaxView
from user.forms import RegistrationForm
from user.models import User
from user.models import users


class LogoutView(BaseLogoutView):
    pass


class LoginView(BaseLoginView):
    template_name = 'user/login.html'


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            template_name='user/register.html',
            context={
                'form': RegistrationForm()
            }
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return self.get(request)

        user = users().create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
        )

        login(request, user)
        return redirect('post:view_posts')


def register_view(request: HttpRequest) -> HttpResponse:
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = users().create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
        )
        login(request, user)
        return redirect('post:view_posts')

    return render(
        request,
        template_name='user/register.html',
        context={
            'form': form
        }
    )


class PasswordChangeView(LoginRequiredMixin, BasePasswordChangeView):
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('post:view_posts')


class ShowUserView(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'user/userdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        profile = context['profile']
        profile.is_followed = profile.followers.filter(pk=self.request.user.pk).exists()

        return context


class UserListView(ListView):
    template_name = 'user/userlist.html'
    context_object_name = 'users'

    def get_user(self) -> User:
        return users().get(pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            raise Http404('userlist empty')
        else:
            return super().dispatch(request, *args, **kwargs)


class FollowersView(UserListView):

    def get_queryset(self):
        return self.get_user().followers.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        info = {'info': f'{self.get_user().username.capitalize()}\'s followers'}
        return context_data | info


class FollowingView(UserListView):

    def get_queryset(self):
        return self.get_user().following.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        info = {'info': f'{self.get_user().username.capitalize()} is following'}
        return context_data | info


class FollowUserView(AjaxView):

    def okay_response(self, user: User, pk: int, **kwargs):
        return super().okay_response(
            user,
            pk,
            following=user.following.filter(pk=pk).exists(),
            **kwargs
        )

    def update_db(self, user: User, pk: int):
        user.click_follow(pk)


class FollowNumbersView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        user = request.user
        data = json.loads(request.body)
        pk = data['pk']

        return JsonResponse({})


