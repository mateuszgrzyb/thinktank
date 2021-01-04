from django.urls import path

from post.views import CreatePost, UpdatePost, DeletePost


def none(): pass


urlpatterns = [
    path('view/<int:pk>', none, name='view_post'),
    path('create/', CreatePost.as_view(), name='create_post'),
    path('update/<int:pk>', UpdatePost.as_view(), name='update_post'),
    path('delete/<int:pk>', DeletePost.as_view(), name='delete_post'),
]
