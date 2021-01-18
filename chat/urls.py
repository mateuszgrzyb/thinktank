from django.urls import path
from .views import GroupChatSelectionView
from .views import RoomView
from .views import AnonRoomView
from .views import PrivChatSelectionView
from .views import PrivChatView

app_name = 'chat'
urlpatterns = [
    path('groupchat/', GroupChatSelectionView.as_view(), name='groupchat_select'),
    path('chat/<str:room>', RoomView.as_view(), name='room'),
    path('anonchat/<str:room>', AnonRoomView.as_view(), name='anon'),

    path('privchat/', PrivChatSelectionView.as_view(), name='privchat_select'),
    path('privchat/<int:pk>', PrivChatView.as_view(), name='privchat'),
]
