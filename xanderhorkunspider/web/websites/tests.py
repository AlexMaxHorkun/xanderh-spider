__author__ = 'Alexander Gorkun'
__email__ = 'mindkilleralexs@gmail.com'

from datetime import datetime, timedelta

from django.test import TestCase

from xanderhorkunspider.web.websites import domain
from xanderhorkunspider.web.websites import models


class WebsitesDomainTestCase(TestCase):
    """
    Testing websites domain, which is used to manage websites, pages and loadings.
    """
    __most_recent_loadings = set()

    def setUp(self):
        """Creating website, pages and loadings for testing"""
        test_website = models.WebsitesModel()
        test_website.host = "www.example.com"
        test_website.name = "Example"
        test_website.save()
        test_page = models.PageModel.objects.create(url="http://www.example.com", website=test_website)
        now = datetime.now()
        test_loading1 = models.LoadingModel.objects.create(
            page=test_page,
            success=True,
            content="test1",
            loading_time=5,
            time=now
        )
        test_loading2 = models.LoadingModel.objects.create(
            page=test_page,
            success=True,
            content="test2",
            loading_time=6,
            time=now
        )
        self.__most_recent_loadings.add(test_loading1)
        self.__most_recent_loadings.add(test_loading2)
        couple_days_ago = now - timedelta(days=3)
        test_loading3 = models.LoadingModel.objects.create(
            page=test_page,
            success=True,
            content="test3",
            loading_time=6,
            time=couple_days_ago
        )

    def test_find_last_loadings(self):
        last_loadings = domain.websites_domain.find_last_loadings(len(self.__most_recent_loadings))
        self.assertEqual(self.__most_recent_loadings, last_loadings)