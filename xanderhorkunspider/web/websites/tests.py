__author__ = 'Alexander Gorkun'
__email__ = 'mindkilleralexs@gmail.com'


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
        test_loading1 = models.LoadingModel.objects.create(
            page=test_page,
            success=True,
            content="test1",
            loading_time=5
        )
        test_loading2 = models.LoadingModel.objects.create(
            page=test_page,
            success=True,
            content="test2",
            loading_time=6
        )
        test_loading3 = models.LoadingModel.objects.create(
            page=test_page,
            success=True,
            content="test3",
            loading_time=6
        )
        self.__most_recent_loadings.add(test_loading2)
        self.__most_recent_loadings.add(test_loading3)

    def test_find_last_loadings(self):
        """Testing method which finds the most recent loadings"""
        last_loadings = domain.websites_domain.find_last_loadings(len(self.__most_recent_loadings))
        self.assertEqual(set(last_loadings), self.__most_recent_loadings)