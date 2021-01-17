from django.http import HttpRequest
from django.urls import reverse


def back_url(request: HttpRequest) -> str:
    prev = 'prev_url'
    prever = 'prever_url'
    default_url = reverse('chat:home')

    referer_url = request.META.get('HTTP_REFERER')

    prever_url = request.session.get(prever, default_url)
    prev_url = request.session.get(prev, default_url)
    curr_url = request.get_full_path()

    # print(f'{prever_url=}\n{prev_url=}\n{curr_url=}\n')

    if curr_url == prev_url:
        prev_url = prever_url

    request.session[prev] = curr_url
    request.session[prever] = prev_url

    request.session['back'] = referer_url

    return referer_url
