__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from xanderhorkunspider import domain as __domain
from xanderhorkunspider.web.websites import models as __models
from xanderhorkunspider import spider as __spider

__websites_dao = __models.WebsitesDBDao()
__pages_dao = __models.PagesDBDao()
__loading_dao = __models.LoadingDBDao()
websites_domain = __domain.Websites(__pages_dao, __websites_dao, __loading_dao)

spider_manager = __spider.SpiderManager(websites_domain, max_p=50, autostart=False)