from django.urls import path

from .views import EmailChangeView, UpdateUserView

app_name = 'settings'
urlpatterns = [
    path('', UpdateUserView.as_view(), name='update_user'),
    path('change_email/', EmailChangeView.as_view(), name='change_email'),
    path('change_email/<uuid:conf_uuid>/', EmailChangeView.as_view(), name='change_email'),
]
