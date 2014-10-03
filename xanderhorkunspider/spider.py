__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from xanderhorkunspider import loader
from xanderhorkunspider import parser
from xanderhorkunspider import models


class Spider(object):
    """
    Gets page content, parses it for new links.
    """
    page_loader = loader.Loader()
    links_parser = parser.OwnLinksParser()

    def __init__(self, ldr=None, links_parser=None):
        """
        :param ldr: Custom Loader impl if needed.
        :param links_parser: Custom LinksParser impl if needed
        """
        if not ldr is None:
            self.page_loader = ldr
        if not links_parser is None:
            self.links_parser = links_parser

    def crawl_on_page(self, page):
        """
        Loads page, gets it's content and new links.
        :param page: Page entity.
        :return: Resulting Loading entity and links list.
        """
        load_result = self.page_loader.load(page.url)
        content = ""
        if not load_result is None:
            content = load_result.body
        loading = models.Loading(page, not load_result is None, content)
        if len(content):
            links = self.links_parser.parse(loading)
        else:
            links = None
        return loading, links