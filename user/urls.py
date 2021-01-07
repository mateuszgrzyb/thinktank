from django.urls import path

from user.views import LoginView
from user.views import LogoutView
from user.views import PasswordChangeView
from user.views import RegisterView
from user.views import ShowUserView
from user.views import FollowersView
from user.views import FollowingView
from user.views import FollowUserView


app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('show/<int:pk>', ShowUserView.as_view(), name='show_user'),
    path('followers/<int:pk>', FollowersView.as_view(), name='followers'),
    path('following/<int:pk>', FollowingView.as_view(), name='following'),
    path('follow_user', FollowUserView.as_view(), name='follow_user')
]
