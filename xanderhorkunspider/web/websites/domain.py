__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from xanderhorkunspider import domain
from xanderhorkunspider.web.websites import models
from xanderhorkunspider import spider

__websites_dao = models.WebsitesDBDao()
__pages_dao = models.PagesDBDao()
__loading_dao = models.LoadingDBDao()
websites_domain = domain.Websites(__pages_dao, __websites_dao, __loading_dao)


class SpiderFactory(object):
    spiders = []
    websites = None
    max_processes = None

    def __init__(self, def_websites, def_max_p=10):
        """
        Creates and stores SpiderManager instances.
        :param def_websites: Default Websites domain object to create spiders.
        :param def_max_p: Default max processes amount for spiders.
        """
        assert isinstance(def_websites, domain.Websites)
        assert def_max_p > 0
        self.websites = def_websites
        self.max_processes = def_max_p

    def create_spider(self, websites=None, max_p=None, autostart=False):
        """
        Creates a spider.
        :param websites: Websites domain obj, if none given default will be used.
        :param max_p: Max amount of processes, if not given default will be used.
        :param autostart: Will the spider be already started? False by default.
        :return: SpiderManager instance.
        """
        if not websites:
            websites = self.websites
        if not max_p:
            max_p = self.max_processes
        spdr = spider.SpiderManager(websites, max_p=max_p, autostart=autostart)
        self.spiders.append(spdr)
        return spdr

    def find_spider_by_id(self, sid):
        """
        Finds spider by it's ID received by "id" function.
        :param sid: Integer
        :return: None or spider.
        """
        sid = int(sid)
        for spdr in self.spiders:
            if id(spdr) == sid:
                return spdr
        return None


spider_factory = SpiderFactory(websites_domain)