__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from xanderhorkunspider import dao


class InMemoryPageDao(dao.PageDao):
    """
    Just keeps Pages in array.
    """
    __pages = {}

    def find_by_url(self, url):
        for p in self.__pages:
            if p.url == url:
                return p
        return None

    def persist(self, page):
        assert page.id == 0
        page.id = id(page)
        self.__pages[page.id] = page


class InMemoryLoadingDao(dao.LoadingDao):
    """
    Just keeps Loadings in array.
    """
    __loadings = {}

    def persist(self, loading):
        assert loading.id == 0
        self.__loadings[id(loading)] = loading

    def save(self, loading):
        """No need to do anything"""
        pass

    def find_all(self, limit=0, offset=0):
        loadings=[]
        for lid, l in self.__loadings:
            loadings.append(l)
        if offset > 0:
            loadings=loadings[offset:]
        if limit > 0:
            loadings=loadings[:limit]
        return loadings


class InMemoryWebsiteDao(dao.WebsiteDao):
    """
    Keeps Websites in array.
    """
    __websites = {}

    def persist(self, website):
        assert website.id == 0
        self.__websites[id(website)] = website

    def save(self, website):
        """No need to do anything"""
        pass