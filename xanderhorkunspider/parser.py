__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

import urllib.parse
import re


class LinksParser:
    """
    Gets links out of html.
    """

    def _validateurl(self, page, url):
        """
        Validates received urls.

        :param page: Page object.
        :param url: link
        :return: true or false
        """
        urldata = urllib.parse.urlparse(url)
        return urldata.scheme in ('http', 'https')

    def parse(self, loading):
        match = re.findall(r'<a\s.*?href="(.*?)".*?>', loading.content)
        urls = set()
        page_url_data=urllib.parse.urlparse(loading.page.url)
        for url in match:
            if url.startswith("/"):
                url = page_url_data.scheme+"://"+page_url_data.netloc + url

            elif not (url.startswith('http://') or url.startswith('https://')):
                if not loading.page.url.endswith('/'):
                    url = '/' + url
                url = loading.page.url + url
            if self._validateurl(loading, url):
                urls.add(url)
        return urls


class OwnLinksParser(LinksParser):
    """
    Allows only links referencing same host
    """

    def _validateurl(self, loading, url):
        valid = super()._validateurl(loading, url)
        if valid:
            return urllib.parse.urlparse(url).netloc.endswith(loading.page.website.host)
        return valid