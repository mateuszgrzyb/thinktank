from django.urls import path

from user.views import LoginView, register_view, LogoutView, PasswordChangeView

urlpatterns = [
    path('login/',           LoginView.as_view(),          name='login'),
    path('register/',        register_view,                name='register'),
    path('logout/',          LogoutView.as_view(),         name='logout'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
]
