__author__ = 'Alexander Gorkun'
__email__ = 'mindkilleralexs@gmail.com'


class PageDao(object):
    """
    Interface of Page entity's DAO.
    """

    def persist(self, page):
        """
        Persist new Page entity.
        :param page: Page entity.
        :return: nothing.
        """
        raise NotImplementedError()

    def find_by_url(self, url):
        """
        Looks for Page entity with such URL.
        :param url: URL property that needed Page entity has.
        :return: Page entity or None.
        """
        raise NotImplementedError()

    def find(self, id):
        """
        Looks for Page entity with such ID.
        :param id: ID of needed entity.
        :return: Page or None.
        """
        raise NotImplementedError()

    def save(self, page):
        """
        Save changes to the Page entity.
        :param page: Page entity.
        """
        raise NotImplementedError()

    def delete(self, page):
        """
        Deletes page entity.
        :param page: Page's ID.
        """
        raise NotImplementedError()


class WebsiteDao(object):
    """
    Interface to Website entity's DAO.
    """

    def persist(self, website):
        """
        Persist new Website entity.
        :param website: Website entity.
        :return: nothing.
        """
        raise NotImplementedError()

    def find_by_url(self, url):
        """
        Looks for Website entity which owns URL.
        :param url: URL address.
        :return: Website entity or None.
        """
        raise NotImplementedError()

    def find(self, id):
        """
        Looks for Website entity with such ID.
        :param id: ID of needed entity.
        :return: Website or None.
        """
        raise NotImplementedError()

    def find_all(self, offset=0, limit=0):
        """
        Gets list of Websites.
        :param offset: Start index.
        :param limit: Max amount to return.
        :return: List.
        """
        raise NotImplementedError()

    def save(self, website):
        """
        Save changes to the Website entity.
        :param website: Website entity.
        """
        raise NotImplementedError()

    def delete(self, wid):
        """
        Deletes a website.
        :param wid: Website's ID.
        """
        raise NotImplementedError()


class LoadingDao(object):
    """
    Interface of Loading entity's DAO.
    """

    def persist(self, loading):
        """
        Persist new Loading entity.
        :param loading: Loading entity.
        :return: nothing.
        """
        raise NotImplementedError()

    def find_by_url(self, url):
        """
        Looks for Loading entity with such Page's URL.
        :param url: URL property of Page that needed Loading entity has.
        :return: Loading entity or None.
        """
        raise NotImplementedError()

    def find(self, id):
        """
        Looks for Loading entity with such ID.
        :param id: ID of needed entity.
        :return: Loading or None.
        """
        raise NotImplementedError()

    def save(self, loading):
        """
        Save changes to the Loading entity.
        :param loading: Loading entity.
        """
        raise NotImplementedError()

    def find_all(self, limit=0, offset=0):
        """
        Gets list of Loadings from storage.
        :param limit: Max amount of entities to return.
        :param offset: Start index.
        :return: List of Loadings.
        """
        raise NotImplementedError()