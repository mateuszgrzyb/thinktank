import uuid
from dataclasses import dataclass
from threading import Thread
from typing import Type
from typing import TypeVar

from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.core.mail import send_mail
from django.forms import Form
from django.forms import ModelForm
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView

from thinktank.mixins import BackUrlMixin
from user.forms import RegistrationForm
from user.forms import UpdateUserForm
from user.models import User
from user.models import users


class LogoutView(BackUrlMixin, BaseLogoutView):
    pass


class LoginView(BackUrlMixin, BaseLoginView):
    template_name = 'user/login.html'

    def form_invalid(self, form):
        print(form.errors)
        print(form.non_field_errors())
        return super().form_invalid(form)


class RegisterView(BackUrlMixin, FormView):
    template_name = 'user/register.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        print('form valid')
        user = form.save()

        login(self.request, user)
        return redirect('post:view_popular')


class PasswordChangeView(BackUrlMixin, LoginRequiredMixin, BasePasswordChangeView):
    template_name = 'user/profile_settings/change_password.html'
    # success_url = reverse_lazy('post:view_posts')


class ShowUserView(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'user/userdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        profile = context['profile']
        upk = self.request.user.pk
        profile.is_followed = profile.followers.filter(pk=upk).exists()

        return context


class UserListView(ListView):
    template_name = 'user/userlist.html'
    context_object_name = 'users'
    info: str

    def get_user(self) -> User:
        return users().get(pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            raise Http404('userlist empty')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        info = {'info': f'{self.get_user().username.capitalize()}{type(self).info}'}
        return context_data | info


class FollowersView(UserListView):
    info = "'s followers"

    def get_queryset(self):
        return self.get_user().followers.all()


class FollowingView(UserListView):
    info = ' is following'

    def get_queryset(self):
        return self.get_user().following.all()


class UpdateUserView(LoginRequiredMixin, BackUrlMixin, TemplateView):
    template_name = 'user/profile_settings.html'

    ac = {
        'name': 'form',
        'cp_value': 'cp',
        'uu_value': 'uu'
    }

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            'uu_form': UpdateUserForm(instance=self.request.user),
            'cp_form': PasswordChangeForm(user=self.request.user),
        } | self.ac

    T = TypeVar('T', Form, ModelForm)

    def validate_form(self, form_class: Type[T], **kwargs) -> T:
        form = form_class(**kwargs)
        if form.is_valid() and form.has_changed():
            self.success = True
            form.save()

        return form

    @dataclass
    class Switch:
        uu_form: UpdateUserForm
        cp_form: PasswordChangeForm

    def post(self, *args, **kwargs):
        self.success = False
        data = self.request.POST
        user = self.request.user

        switch = {
            self.ac['uu_value']: lambda: self.Switch(
                self.validate_form(UpdateUserForm, data=data, instance=user),
                PasswordChangeForm(user=user),
            ),
            self.ac['cp_value']: lambda: self.Switch(
                UpdateUserForm(instance=user),
                self.validate_form(PasswordChangeForm, data=data, user=user),
            )
        }

        return render(
            self.request,
            self.template_name,
            context={'success': self.success} | vars(switch[data[self.ac['name']]]()) | self.ac
        )


class EmailChangeView(LoginRequiredMixin, View):
    conf_uuid = None
    email = None

    def get_url(self) -> str:
        return self.request.build_absolute_uri(
            reverse("user:confirm_email", kwargs={'conf_uuid': self.conf_uuid})
        )

    def get(self, request: HttpRequest, conf_uuid: uuid) -> HttpResponse:
        if conf_uuid == self.conf_uuid:
            request.user.email = self.email
            request.user.save()

            result = HttpResponse('okay')
        else:
            result = HttpResponse(f'''
            uuid from url: {conf_uuid}
            saved uuid: {self.conf_uuid}
            ''')

        self.email = None
        self.conf_uuid = None

        return result

    def post(self, request: HttpRequest) -> HttpResponse:
        self.email = request.POST['email']
        self.conf_uuid = uuid.uuid4()

        Thread(
            target=send_mail,
            kwargs={
                'subject': 'ThinkTank: Change your email',
                'message': f'please change your email god dammit: \n{self.get_url()}\n',
                'from_email': None,
                'recipient_list': [self.email],
            },
        ).start()

        return HttpResponse('okay')
