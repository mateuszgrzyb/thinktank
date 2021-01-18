from abc import abstractmethod

from thinktank.helpers import back_url


class SuccessUrlNextPageMixin:
    @abstractmethod
    def get_back_url(self):
        pass

    def get_next_page(self):
        return self.get_back_url()

    def get_success_url(self):
        return self.get_back_url()


class BackUrlMixin(SuccessUrlNextPageMixin):
    def get_back_url(self):
        return back_url(self.request)

