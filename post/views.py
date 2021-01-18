from abc import ABC

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from post.mixins import UserIsOwnerMixin
from post.models import Post
from thinktank.mixins import BackSuccessUrlNextPageMixin


class CreatePost(
    BackSuccessUrlNextPageMixin,
    LoginRequiredMixin,
    CreateView
):
    model = Post
    fields = [
        'content'
    ]

    template_name = 'post/createpost.html'

    # success_url = reverse_lazy('post:view_posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePost(
    BackSuccessUrlNextPageMixin,
    UserIsOwnerMixin,
    UpdateView
):
    model = Post
    fields = [
        'content'
    ]
    template_name = 'post/updatepost.html'
    # success_url = reverse_lazy('post:view_posts')


class DeletePost(
    BackSuccessUrlNextPageMixin,
    UserIsOwnerMixin,
    DeleteView
):
    model = Post
    # success_url = reverse_lazy('post:view_posts')
    template_name = 'post/deletepost.html'


class ViewPosts(ListView):
    model = Post
    paginate_by = 3
    template_name = 'post/viewposts.html'
    ordering = '-pk'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        for post in context[self.context_object_name]:
            post.liked = post.likes.filter(pk=self.request.user.pk).exists()
        return context


class ViewFollowingPosts(ViewPosts):
    def get_queryset(self):
        user = self.request.user
        objects = self.model.objects
        authors = user.following.values('pk')

        return objects.filter(author__in=authors)


class ViewPopularPosts(ViewPosts):
    pass
