__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

import datetime


class Website:
    """
    Holds data about added websites to parse.
    """
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
    url = ""
    content = None
    _loaded = None
    website = None

    def __init__(self, website, url, content=None, loaded=None):
        """
        Initiates obj with it's url and other attrs.

        :param url: Address.
        :param website: Website that this page belongs.
        :param content: Response body.
        :param loaded: last time loaded.
        """
        self.url = url
        self.content = content
        self.loaded = loaded
        self.website = website
        website.pages.add(self)

    @property
    def loaded(self):
        return self._loaded

    @loaded.setter
    def loaded(self, value):
        """
        Checks if given value is datetime or None.

        :param value: new 'loaded' value
        :return:
        """
        if isinstance(value, datetime.datetime) or value is None:
            self._loaded = value
        else:
            raise ValueError("Loaded attribute can be only a datetime instance or None")