__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

import datetime


class Website(object):
    """
    Holds data about added websites to parse.
    """
    id = 0
    name = ""
    pages = set()
    host = ""

    def __init__(self, name, host):
        """
        :param name: Website's name.
        :param host: host that all relative pages share.
        """
        self.name = name
        self.host = host


class Page(object):
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
        loading = self.get_last_successful_loading()
        if not loading is None:
            return loading.content
        else:
            return None

    def get_last_successful_loading(self):
        last_loading = None
        for l in self.loadings:
            if l.success and (last_loading is None or last_loading.time < l.time):
                last_loading = l
        if last_loading:
            return last_loading
        else:
            return None


class Loading(object):
    """
    Holds info about a loading attempt.
    """
    id = 0
    page = None
    success = False
    headers = {}
    content = ""
    time = None

    def __init__(self, page, success, headers={}, content="", time=datetime.datetime.now()):
        """
        :param page: link to Page object.
        :param success: Whether page loading was successful.
        :param headers: Headers dict.
        :param content: Page's content (HTML).
        :param time: Date and time when loading was finished.
        """
        self.content = content
        self.headers = dict((k.lower(), v.lower) for k, v in headers.items())
        self.page = page
        if self not in page.loadings:
            page.loadings.append(self)
        self.success = success
        self.time = time