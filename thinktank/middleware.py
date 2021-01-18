from typing import Callable

from django.http import HttpRequest
from django.http import HttpResponse

from thinktank.helpers import back_url


class BackMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)



