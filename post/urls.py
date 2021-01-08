from django.urls import path

from post.views import CreatePost
from post.views import DeletePost
from post.views import UpdatePost
from post.views import ViewPosts


app_name = 'post'
urlpatterns = [
    path('view/', ViewPosts.as_view(), name='view_posts'),
    path('create/', CreatePost.as_view(), name='create_post'),
    path('update/<int:pk>', UpdatePost.as_view(), name='update_post'),
    path('delete/<int:pk>', DeletePost.as_view(), name='delete_post'),
]
