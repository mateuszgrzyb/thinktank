from django.urls import path

from user.views import EmailChangeView
from user.views import LoginView
from user.views import LogoutView
from user.views import PasswordChangeView
from user.views import RegisterView
from user.views import ShowUserView
from user.views import FollowersView
from user.views import FollowingView
#from user.views import UpdateUserView
from user.views import UpdateUserView

app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('change_email/', EmailChangeView.as_view(), name='change_email'),
    path('change_email/<uuid:conf_uuid>', EmailChangeView.as_view(), name='confirm_email'),

    path('show/<int:pk>', ShowUserView.as_view(), name='show_user'),

    path('followers/<int:pk>', FollowersView.as_view(), name='followers'),
    path('following/<int:pk>', FollowingView.as_view(), name='following'),

    path('update/<int:pk>', UpdateUserView.as_view(), name='update')
]
