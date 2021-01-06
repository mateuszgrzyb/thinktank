import json

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.http import HttpRequest
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from post.mixins import UserIsOwnerMixin
from post.models import Post
from post.models import posts
from user.models import User


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'content'
    ]

    template_name = 'post/createpost.html'
    success_url = reverse_lazy('post:view_posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePost(UserIsOwnerMixin, UpdateView):
    model = Post
    fields = [
        'content'
    ]
    template_name = 'post/updatepost.html'
    success_url = reverse_lazy('post:view_posts')


class DeletePost(UserIsOwnerMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post:view_posts')


class ViewPosts(ListView):
    model = Post
    paginate_by = 3
    template_name = 'post/viewposts.html'


class LikePost(View):

    def post(self, request: HttpRequest) -> JsonResponse:

        user: User = request.user
        data = json.loads(request.body)
        pk = data['like']

        def okay_response():

            likes = posts().get(pk=pk).likes

            return JsonResponse({
                'response': 'okay',
                'likes': likes.count(),
                'user': likes.filter(pk=user.pk).exists()
            })

        if data['type'] == 'fetch':

            return okay_response()

        elif data['type'] == 'update':
            if user.is_anonymous:
                return JsonResponse({'response': 'error'})
            else:
                user.click_like(pk)

            return okay_response()

        else:
            raise Exception("Bad ajax request type")
