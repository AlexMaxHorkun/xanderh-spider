__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from xanderhorkunspider import dao


class InMemoryPageDao(dao.PageDao):
    pages={}

    def find_by_url(self, url):
        for p in self.pages:
            if p['object'].url==url:
                return p['object']
        return None

    def persist(self, page):
        assert page.id==0
        page.id=id(page)
        self.pages[page.id]=page