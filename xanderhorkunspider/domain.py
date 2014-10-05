__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'


class Websites(object):
    _page_dao = None
    _website_dao = None
    _loading_dao = None

    def __init__(self, page_dao, website_dao, loading_dao):
        """
        :param page_dao: PageDao impl.
        :param website_dao: WebsiteDao impl.
        :param loading_dao: LoadingDao impl.
        """
        self._page_dao = page_dao
        self._website_dao = website_dao
        self._loading_dao = loading_dao

    def persist(self, website):
        """
        Saves Website entity, it's pages and it's pages' loadings.
        :param website: Website obj.
        """
        self._website_dao.persist(website)
        for page in website.pages:
            self._page_dao.persist(page)
            for loading in page.loadings:
                self._loading_dao.persist(loading)

    def find(self, wid):
        return self._website_dao.find(wid)

    def save_loading(self, loading):
        if not loading.page:
            raise ValueError("Loading must have link to page")
        if loading.page.id == 0:
            self._page_dao.persist(loading.page)
        if loading.id == 0:
            self._loading_dao.persist(loading)
        else:
            self._loading_dao.save(loading)

    def find_page_by_url(self, url):
        return self._page_dao.find_by_url(url)