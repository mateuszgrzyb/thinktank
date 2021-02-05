from django.urls import include, path

# from user.views import EmailChangeView
from user.views import LoginView
from user.views import LogoutView
# from user.views import PasswordChangeView
from user.views import RegisterView
from user.views import UserDetailView
from user.views import FollowersView
from user.views import FollowingView
# from user.views import UpdateUserView

app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('show/<int:pk>', UserDetailView.as_view(), name='show_user'),
    path('followers/<int:pk>', FollowersView.as_view(), name='followers'),
    path('following/<int:pk>', FollowingView.as_view(), name='following'),

    path('settings/', include('settings.urls', namespace='settings')),
]
