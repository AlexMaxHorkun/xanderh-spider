__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

import requests


class LoadResult(object):
    url = ""
    headers = {}
    body = ""

    def __init__(self, url, headers, body):
        """
        Initialize object with information about loaded page.

        :type url str
        :type headers dict
        :type body str
        """
        self.url = url
        self.headers = headers
        self.body = body


class Loader(object):
    timeout = 5

    def __init__(self, timeout=0):
        """
        :param timeout: max amount of time to load pages
        """
        if timeout:
            self.timeout = int(timeout)

    def load(self, url, timeout=None):
        """
        Loads page content.

        :param url: URL address.
        :param timeout: max amount of time to load page within, optional.
        :return: page headers and body in LoadResult obj or None if loading failed.
        """
        if timeout is None and self.timeout is not None:
            timeout = self.timeout

        try:
            http_response = requests.get(url, timeout=timeout)
        except:
            return None
        if not http_response:
            return None
        return LoadResult(url, http_response.headers, http_response.text)