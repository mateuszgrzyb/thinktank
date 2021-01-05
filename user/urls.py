from django.urls import path

from user.views import LoginView
from user.views import LogoutView
from user.views import PasswordChangeView
from user.views import RegisterView

app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
]
