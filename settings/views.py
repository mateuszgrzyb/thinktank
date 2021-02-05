import uuid
from dataclasses import dataclass
from threading import Thread
from typing import Type, TypeVar

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.forms import Form, ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from thinktank.mixins import BackUrlMixin
from .forms import UpdateUserForm


class UpdateUserView(LoginRequiredMixin, BackUrlMixin, TemplateView):
    template_name = 'settings/update_user.html'

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conf_uuid = None
        self.email = None

    def get_url(self, conf_uuid) -> str:
        return self.request.build_absolute_uri(
            reverse("user:settings:change_email", kwargs={'conf_uuid': conf_uuid})
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
                'message': f'please change your email god dammit: \n{self.get_url(self.conf_uuid)}\n',
                'from_email': None,
                'recipient_list': [self.email],
            },
        ).start()

        return HttpResponse('okay')

