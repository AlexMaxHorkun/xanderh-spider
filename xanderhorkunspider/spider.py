__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from xanderhorkunspider import loader
from xanderhorkunspider import parser
from xanderhorkunspider import models


class LoadingEvaluator(object):
    def evaluateLoading(self, loading):
        """
        Determines whether page content is worth while.
        :param loading: Loading object.
        :return: Bool.
        """
        return 'content-type' in loading.headers and loading.headers['content-type'] == 'text/html'


class Spider(object):
    """
    Gets page content, parses it for new links.
    """
    page_loader = loader.Loader()
    links_parser = parser.OwnLinksParser()

    def __init__(self, ldr=None, links_parser=None):
        """
        :param ldr: Custom Loader impl if needed.
        :param links_parser: Custom LinksParser impl if needed.
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
        loading = models.Loading(page, not load_result is None, getattr(load_result, "headers", {}),
                                 getattr(load_result, "body", ""))
        if len(loading.content):
            links = self.links_parser.parse(loading)
        else:
            links = None
        return loading, links


class SpiderManager(object):
    spider = Spider()

    def __init__(self, spider=None):
        """
        :param spider: Custom Spider impl if needed.
        """
        if spider is not None:
            self.spider = spider