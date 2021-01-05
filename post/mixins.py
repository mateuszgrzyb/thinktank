from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic.detail import SingleObjectMixin


class UserIsOwnerMixin(LoginRequiredMixin, UserPassesTestMixin, SingleObjectMixin):
    def test_func(self):
        author = self.get_object().author
        user = self.request.user
        return author.pk == user.pk

    def handle_no_permission(self):
        response = HttpResponse(
            'You are not the owner of this content'
        )
        return super().handle_no_permission()
