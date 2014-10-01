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

    def parse(self, page):
        match=re.findall(r'<a\s.*?href="(.*?)".*?>', page.content)
        urls=set()
        for url in match:
            if url.startswith("/"):
                url=urllib.parse.urlparse(page.url).netloc+url

            elif not (url.startswith('http://') or url.startswith('https://')):
                if not page.url.endswith('/'):
                    url='/'+url
                url=page.url+url
            if self._validateurl(page, url):
                urls.add(url)
        return urls


class OwnLinksParser(LinksParser):
    """
    Allows only links referencing same host
    """
    def _validateurl(self, page, url):
        valid=super()._validateurl(page, url)
        if valid:
            return urllib.parse.urlparse(url).netloc.endswith(page.website.host)
        return valid