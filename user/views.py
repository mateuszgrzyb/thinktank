from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView, \
    PasswordChangeView as BasePasswordChangeView
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import DetailView, FormView, ListView

from thinktank.mixins import BackUrlMixin
from user.forms import RegistrationForm
from user.models import User, users


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


# class PasswordChangeView(BackUrlMixin, LoginRequiredMixin, BasePasswordChangeView):
#     template_name = 'user/profile_settings/change_password.html'
#     # success_url = reverse_lazy('post:view_posts')


class UserDetailView(DetailView):
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


