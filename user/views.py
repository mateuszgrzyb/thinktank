from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.views.generic import DetailView

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
    template_name = 'user/show_user.html'