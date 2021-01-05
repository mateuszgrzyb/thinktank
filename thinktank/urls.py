
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls', namespace='chat')),
    path('user/', include('user.urls', namespace='user')),
    path('post/', include('post.urls', namespace='post')),
]
