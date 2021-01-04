from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, SingleObjectMixin
from django.views.generic.edit import BaseFormView

from post.models import Post


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'content'
    ]

    template_name = 'post/createpost.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UserIsOwnerMixin(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SingleObjectMixin
):
    def test_func(self):
        author = self.get_object().author
        user = self.request.user
        return author.pk == user.pk

    # def handle_no_permission(self):
    #     return HttpResponse(
    #         'You are not the owner of this content'
    #     )


class UpdatePost(UserIsOwnerMixin, UpdateView):
    model = Post
    fields = [
        'content'
    ]
    template_name = 'post/updatepost.html'
    success_url = reverse_lazy('home')


class DeletePost(UserIsOwnerMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')
