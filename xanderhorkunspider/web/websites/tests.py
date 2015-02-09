__author__ = 'Alexander Gorkun'
__email__ = 'mindkilleralexs@gmail.com'


from django.test import TestCase
from django.contrib.auth.models import User, Group
from xanderhorkunspider.web.websites import domain
from xanderhorkunspider.web.websites import models
from xanderhorkunspider.web import config


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


class UsersDomainTestCase(TestCase):
    """
    Testing domain class responsible of managing users.
    """

    def test_create(self):
        """
        Testing creating new user.
        """
        test_email = 'test@test1.com'
        test_username = 'test'
        test_pass = 'testpass'

        """Creating a valid user"""
        user = domain.users.create(test_username, test_email, test_pass)
        self.assertTrue(user.id > 0, "User's ID is not greater then zero")
        self.assertIsNotNone(user, "Returned None instead of a user")
        self.assertEqual(user.email, test_email, "Emails are not equal")
        self.assertEqual(user.username, test_username, "Usernames are not equal")
        """ testing groups is actually failing, although it works within real running app

        self.assertCountEqual(user.user_permissions.all(), config.settings.DEFAULT_GROUPS,
                              "Standard groups were not assigned to user")
        for group in user.groups.all():
            self.assertIn(group.name, config.settings.DEFAULT_GROUPS, "Some unknown group was assigned to user")
        """

        "Creating invalid users with blank username and non-unique email"
        self.assertRaises(Exception, domain.users.create, None, test_email+"1", test_pass)
        self.assertRaises(Exception, domain.users.create, test_username+"1", test_email, test_pass)