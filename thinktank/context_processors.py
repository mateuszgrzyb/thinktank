from django.http import HttpRequest
from django.urls import reverse

from thinktank.helpers import back_url


def back_button(request: HttpRequest) -> dict:
    return {
        'back': back_url(request),
        # 'back': prev_url
    }


def parser(welcome: str, links: dict[str, str]) -> dict:
    return {
        'navbar': {
            'welcome': welcome,
            'links': [{'name': k, 'url': v} for k, v in links.items()]
        }
    }


def navbar(request: HttpRequest) -> dict:
    if (u := request.user).is_anonymous:
        welcome = 'Hey anon!'
        links = {
            'Login': reverse('user:login'),
            'Register': reverse('user:register'),
        }
    else:
        welcome = f'Hey, {u.username}!'
        links = {
            'Logout': reverse('user:logout'),
            'Create New Post': reverse('post:create_post'),
            'Profile Settings': reverse('user:settings:update_user'),
        }

        if u.is_superuser:
            links |= {'Admin Panel': reverse('admin:index')}

    return parser(welcome, links)

