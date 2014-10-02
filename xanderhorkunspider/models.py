__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

import datetime


class Website:
    """
    Holds data about added websites to parse.
    """
    id = 0
    homepage = ""
    name = ""
    pages = set()
    host = ""

    def __init__(self, url, name, host):
        """
        :param url: URL address of a main page.
        :param name: Website's name.
        :param host: host that all relative pages share.
        """
        self.homepage = url
        self.name = name
        self.host = host


class Page:
    """
    Holds info about loaded pages.
    """
    id = 0
    url = ""
    website = None
    loadings = []

    def __init__(self, website, url):
        """
        Initiates obj with it's url and other attrs.

        :param url: Address.
        :param website: Website that this page belongs.
        :param content: Response body.
        :param loaded: last time loaded.
        """
        self.url = url
        self.website = website
        website.pages.add(self)

    def isloaded(self):
        """
        Checks if the page's content was successfully loaded at least once.

        :return: bool
        """
        for loading in self.loadings:
            if loading.success:
                return True
        return False

    def getcontent(self):
        """
        Returns content of last successful loading.
        :return: Content (HTML) or None
        """
        last_loading = None
        for l in self.loadings:
            if l.success and (last_loading is None or last_loading.time < l.time):
                last_loading = l
        if last_loading:
            return last_loading.content
        else:
            return None


class Loading:
    """
    Holds info about a loading attempt.
    """
    id = 0
    page = None
    success = False
    content = ""
    time = None

    def __init__(self, page, success, content="", time=datetime.datetime.now()):
        """
        :param page: link to Page object.
        :param success: Whether page loading was successful.
        :param content: Page's content (HTML).
        :param time: Date and time when loading was finished.
        """
        self.content = content
        self.page = page
        if self not in page.loadings:
            page.loadings.append(self)
        self.success = success
        self.time = time