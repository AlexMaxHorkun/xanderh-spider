__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from multiprocessing import process
import threading
import time
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


class CrawlingProcess(threading.Thread):
    page = None
    resulting_loading = None
    resulting_links = None
    finished = False
    spider = None
    websites = None

    def __init__(self, page, spider, websites):
        """
        :param page: Page to crawl on.
        :param websites: Websites.
        :param spider: Spider.
        """
        super().__init__()
        self.page = page
        self.spider = spider
        self.websites = websites

    def run(self):
        """
        Runs spider's crawl and saves results.
        """
        print("crawling on %s" % self.page.url)
        loading, links = self.spider.crawl_on_page(self.page)
        self.resulting_links = links
        self.resulting_loading = loading
        self.websites.saveLoading(loading)
        self.finished = True
        print("finished crawling on %s" % self.page.url)


class SpiderManager(threading.Thread):
    spider = Spider()
    max_process_count = 50
    __processes = []
    websites = None

    def __init__(self, websites, spider=None, max_p=None):
        """
        :param websites: Websites domain.
        :param spider: Custom Spider impl if needed.
        :param max_p: Maximum amount of processes to run.
        """
        super().__init__()
        if spider is not None:
            self.spider = spider
        if isinstance(max_p, int) and max_p > 0:
            self.max_process_count = max_p
        self.websites = websites

    def running_count(self):
        """
        Finds how many crawling processes is running.
        :return: number
        """
        running = 0
        for p in self.__processes:
            if p.is_alive():
                running += 1
        return running

    def crawl(self, page):
        """
        Starts a proccess of crawling on page.
        :param page: Page or url.
        """
        if not isinstance(page, models.Page):
            url = page
            page = self.websites.findPageByUrl(url)
            if page is None:
                page = self.websites.createPageFromUrl(url)
        self.__processes.append(CrawlingProcess(page, self.spider, self.websites))

    def run(self):
        for p in self.__processes:
            print("Checkign processes, having %s" % (len(self.__processes)))
            if not p.is_alive():
                if not p.finished:
                    if self.running_count() < self.max_process_count:
                        p.start()
                else:
                    for l in p.resulting_links:
                        self.crawl(l)
                    self.__processes.remove(p)
            time.sleep(1)

    def terminate(self):
        super().terminate()
        for p in self.__processes:
            p.terminate()
            self.__processes.remove(p)