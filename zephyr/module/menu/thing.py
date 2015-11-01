
from zephyr.breeze import Backend
from zephyr.lib.paginator import Paginator

__all__ = ['MenuThing']


class MenuThing(object):

    def __init__(self):
        self.page_repo = Backend('Page')

    def menu(self, page=1):
        pages = self.page_repo.menu(True)
        return pages

    def update(self, sort):
        for menu_order, pid in enumerate(sort):
            self.page_repo.update_menu_order(pid, menu_order)