__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from xanderhorkunspider import loader
from xanderhorkunspider import parser
from xanderhorkunspider import models
from xanderhorkunspider import domain
import multiprocessing


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


class CrawlingProcess(multiprocessing.Process):
    page=None
    resulting_loading=None
    resulting_links=None
    _process=NoneW



class SpiderManager(object):
    spider = Spider()
    max_process_count=50
    processes={}
    websites=None

    def __init__(self, websites, spider=None, max_p=None):
        """
        :param websites: Websites domain.
        :param spider: Custom Spider impl if needed.
        :param max_p: Maximum amount of processes to run.
        """
        if spider is not None:
            self.spider = spider
        if isinstance(max_p, int) and max_p > 0:
            self.max_process_count=max_p
        self.websites=websites

    def _crawl(self, page):
        """
        Process, runs spider's crawl and saves results.
        :param page: Page entity.
        :return: shit.
        """
        loading, links=self.spider.crawl_on_page(page)
        self.websites.saveLoading(loading)
        if len(links) > 0:
            for l in links:
                self.startCrawlingProcess