
from django.urls import path
from .views import HomeView, RoomView, AnonRoomView

urlpatterns = [
    path('',                    HomeView.as_view(),     name='home'),
    path('anonchat/<str:room>', AnonRoomView.as_view(), name='anon'),
    path('chat/<str:room>',     RoomView.as_view(),     name='room')
]
