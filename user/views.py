from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.views.generic import CreateView, UpdateView


class LogoutView(BaseLogoutView):
    pass


class LoginView(BaseLoginView):
    template_name = 'user/login.html'


class RegisterView(CreateView):
    pass


class ChangePasswordView(UpdateView):
    pass


