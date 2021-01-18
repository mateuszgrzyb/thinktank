from django.contrib import admin
from django.urls import include
from django.urls import path

from thinktank.views import AjaxView
from thinktank.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('chat/', include('chat.urls', namespace='chat')),
    path('user/', include('user.urls', namespace='user')),
    path('post/', include('post.urls', namespace='post')),
    path('ajax/', AjaxView.as_view(), name='ajax'),
    path('admin/', admin.site.urls),
]
