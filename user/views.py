import uuid
from threading import Thread

from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.core.mail import send_mail
from django.forms import Form
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

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
    # model = User
    # fields = ['username', 'email', 'bio']
    template_name = 'user/profile_settings.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        return super().get_context_data(**kwargs) | {
            'uu_form': UpdateUserForm(instance=user),
            'cp_form': PasswordChangeForm(user=user),
        }

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        user = request.user

        if (data := request.POST)['form'] == 'uu':
            form = UpdateUserForm(data=data)
            if form.is_valid():
                print('is valid')
                print(form.has_changed())
            else:
                print(form.errors)

        elif request.POST['form'] == 'cp':
            form = PasswordChangeForm(user=user, data=data)
            if form.is_valid():
                print(form.save())
            else:
                print(form.errors)

        # uu_form = UpdateUserForm(request.POST)
        # cp_form = PasswordChangeForm(user=user, data=request.POST)
        # print(f'uu_form: {uu_form.is_bound}')
        # print(f'cp_form: {cp_form.is_bound}')
        return HttpResponse('a')


class EmailChangeView(LoginRequiredMixin, View):
    conf_uuid: uuid
    email: str

    def get(self, request: HttpRequest, conf_uuid: uuid) -> HttpResponse:
        if conf_uuid == type(self).conf_uuid:
            u = request.user
            u.email = type(self).email
            u.save()
            return HttpResponse('okay')

    def post(self, request: HttpRequest) -> HttpResponse:
        type(self).email = request.POST['email']
        type(self).conf_uuid = uuid.uuid4()
        url = request.build_absolute_uri(
            reverse("user:confirm_email", kwargs={'conf_uuid': type(self).conf_uuid})
        )
        body = f'please change your email god dammit: {url}'

        print('starting thread')

        Thread(
            target=send_mail,
            kwargs={
                'subject': 'ThinkTank: Change your email',
                'message': body,
                'from_email': None,
                'recipient_list': [type(self).email],
            },
        ).start()

        print('thread started')

        return HttpResponse('okay')
