__author__ = 'Alexander Gorkun'
__email__ = 'mindkilleralexs@gmail.com'

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate as django_auth
from django.db import transaction
from django.db.models import Q
from django.core.cache import cache

from xanderhorkunspider import domain
from xanderhorkunspider.web.websites import models
from xanderhorkunspider.web.config import settings
from xanderhorkunspider import spider


__websites_dao = models.WebsitesDBDao()
__pages_dao = models.PagesDBDao()
__loading_dao = models.LoadingDBDao()


class Websites(domain.Websites):
    """
    Class contains business logic related to websites, pages and loadings.
    """

    def find_last_loadings(self, limit=10):
        """
        Gets a list of most recently created loadings.

        :param limit: Max amount of items to return.
        :return: List of Loading models.
        """
        cache_key = 'last_loadings_' + str(10)
        if cache_key in cache:
            return cache.get(cache_key)
        loadings = self._loading_dao.find_all(limit=limit, order_by='time', order_asc=False)
        cache.set(cache_key, loadings, 600)
        return loadings


websites_domain = Websites(__pages_dao, __websites_dao, __loading_dao)


class SpiderFactory(object):
    """
    Creates and stores spiders.
    """

    spiders = []
    websites = None
    max_processes = None

    def __init__(self, def_websites, def_max_p=10):
        """
        Setting default parameters for future spiders.

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


class Users(object):
    """
    Contains business logic to work with users.
    """

    default_groups = set()

    def __init__(self, default_groups=None):
        """
        Class is responsible for maintaining users (creation, authorization etc.)
        :param default_groups: Default groups for all new-created users, set of Group entities.
        """
        if default_groups:
            self.default_groups = set(default_groups)

    def create(self, username, email, password):
        """
        Creates user based on credentials, checks if user with such credentials already exists.
        :param username: User's name.
        :param email: E-mail.
        :param password: User's password.
        :raises ValueError: If user with such credentials already exists.
        :return: User instance.
        """
        if (User.objects.filter(username=username) | User.objects.filter(email=username)).exists():
            raise ValueError("Such user already exists")
        with transaction.atomic():
            user = User.objects.create_user(username, email=email, password=password)
            if user is None:
                raise RuntimeError("Unable to create user for some reasons")
            for group in self.default_groups:
                user.groups.add(group)
        return user

    def authenticate(self, username, password):
        """
        Authenticates user.
        :param username: User's name.
        :param password: Password.
        :return: User instance.
        """
        user = django_auth(username=username, password=password)
        if user and not user.is_active:
            user = None
        return user


__default_groups = Group.objects.filter(Q(name__in=settings.DEFAULT_GROUPS))

users = Users(default_groups=__default_groups)