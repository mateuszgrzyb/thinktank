from django.urls import path

from post.views import CreatePost
from post.views import DeletePost
from post.views import UpdatePost
from post.views import ViewFollowingPosts
from post.views import ViewPopularPosts


app_name = 'post'
urlpatterns = [
    path('view_popular/', ViewPopularPosts.as_view(), name='view_popular'),
    path('view_following/', ViewFollowingPosts.as_view(), name='view_following'),
    path('create/', CreatePost.as_view(), name='create_post'),
    path('update/<int:pk>', UpdatePost.as_view(), name='update_post'),
    path('delete/<int:pk>', DeletePost.as_view(), name='delete_post'),
]
