from django.urls import path

from user.views import LoginView
from user.views import LogoutView
from user.views import PasswordChangeView
from user.views import RegisterView
from user.views import ShowUserView

app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('show/<int:pk>', ShowUserView.as_view(), name='show_user')
]
