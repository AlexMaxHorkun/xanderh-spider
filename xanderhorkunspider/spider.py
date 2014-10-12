__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

import threading
import time

from xanderhorkunspider import loader
from xanderhorkunspider import parser
from xanderhorkunspider import models


class LoadingEvaluator(object):
    def evaluate_loading(self, loading):
        """
        Determines whether page content is worth while.
        :param loading: Loading object.
        :return: Bool.
        """
        return 'content-type' in loading.headers and loading.headers['content-type'] == 'text/html'


class Spider(object):
    """
    Gets page content, parses it for new links.

    If use_existing is True then if content is already loaded
    it will be parsed, not loaded again.
    """
    page_loader = loader.Loader()
    links_parser = parser.LinksParser()
    use_existing = True

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
        if self.use_existing and page.isloaded():
            loading = page.get_last_successful_loading()
        else:
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
    evaluator = None

    def __init__(self, page, spider, websites, ev):
        """
        :param page: Page to crawl on.
        :param websites: Websites.
        :param spider: Spider.
        :param ev: LoadingEvaluator to determine whether to save page or not (if it has ID=0).
        """
        super().__init__()
        self.page = page
        self.spider = spider
        self.websites = websites
        self.evaluator = ev

    def run(self):
        """
        Runs spider's crawl and saves results.
        """
        loading, links = self.spider.crawl_on_page(self.page)
        self.resulting_links = links
        self.resulting_loading = loading
        if (loading.id == 0 and loading.page, id == 0 and self.evaluator.evaluate_loading(loading)) \
                or not loading.page.id == 0:
            self.websites.save_loading(loading)
        self.finished = True


class SpiderManager(threading.Thread):
    spider = Spider()
    max_process_count = 50
    __processes = []
    websites = None
    evaluator = LoadingEvaluator()
    update_existing = False
    stop_when_done = False

    def __init__(self, websites, spider=None, max_p=None, loading_evaluator=None):
        """
        :param websites: Websites domain.
        :param spider: Custom Spider impl if needed.
        :param max_p: Maximum amount of processes to run.
        :param loading_evaluator: LoadingEvaluator custom impl if needed.
        """
        super().__init__()
        if spider is not None:
            self.spider = spider
        self.spider.use_existing = not self.update_existing
        if isinstance(max_p, int) and max_p > 0:
            self.max_process_count = max_p
        self.websites = websites
        if not loading_evaluator is None:
            self.evaluator = loading_evaluator
        self.start()

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

    def is_done(self):
        """
        Check if no processes are running or in queue.
        :return: bool.
        """
        for p in self.__processes:
            if not p.finished:
                return False

        return True

    def crawl(self, page):
        """
        Starts a proccess of crawling on page.
        :param page: Page.
        """
        self.__processes.append(CrawlingProcess(page, self.spider, self.websites, self.evaluator))

    def _start_process(self, crawling_process):
        """
        When finds not yet started crawling process starts it if possible.

        :param crawling_process: CrawlingProcess.
        """
        if self.running_count() < self.max_process_count:
            crawling_process.start()

    def _process_crawling_result(self, crawling_process):
        """
        Processes crawling process when it's finished, creates new
        crawling processes for received links from page's body.

        :param crawling_process: CrawlingProcess
        """
        if crawling_process.resulting_links is not None:
            for l in crawling_process.resulting_links:
                page = self.websites.find_page_by_url(l)
                if page is None:
                    page = models.Page(crawling_process.page.website, l)
                if not page.isloaded() or self.update_existing:
                    self.crawl(page)

    def run(self):
        while True:
            for p in self.__processes:
                if not p.is_alive():
                    if not p.finished:
                        self._start_process(p)
                    else:
                        self._process_crawling_result(p)
                        self.__processes.remove(p)
                if self.stop_when_done and self.is_done():
                    break
            time.sleep(1)