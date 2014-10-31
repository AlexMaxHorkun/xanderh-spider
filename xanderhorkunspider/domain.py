__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from xanderhorkunspider import models


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

    def find_loadings(self, l=0, o=0):
        return self._loading_dao.find_all(limit=l, offset=o)

    def find_websites(self, l=0, o=0):
        """
        Gets list of websites.
        :param l: Max amount of items.
        :param o: Offset.
        :return: List.
        """
        return self._website_dao.find_all(limit=l, offset=o)

    def save(self, website):
        """
        Saves changes to a website.
        :param website: Website entity.
        """
        self._website_dao.save(website)

    def remove(self, website):
        """
        Deletes a website.
        :param website: Website entity or ID.
        """
        wid = 0
        if isinstance(website, models.Website):
            wid = website.id
        else:
            wid = int(website)
        self._website_dao.delete(wid)

    def find_page(self, pid):
        """
        Finds a page by ID.
        :param pid: Page's ID.
        :return: Page.
        """
        return self._page_dao.find(pid)

    def save_page(self, page):
        """
        Persists of saves page.
        :param page: Page entity.
        """
        if page.id:
            self._page_dao.persist(page)
        else:
            self._page_dao.save(page)