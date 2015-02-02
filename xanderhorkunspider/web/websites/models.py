__author__ = 'Alexander Gorkun'
__email__ = 'mindkilleralexs@gmail.com'

import json

from django.db import models

from xanderhorkunspider.models import Website
from xanderhorkunspider.models import Page
from xanderhorkunspider.models import Loading
from xanderhorkunspider.dao import WebsiteDao
from xanderhorkunspider.dao import PageDao
from xanderhorkunspider.dao import LoadingDao


class WebsitesModel(models.Model, Website):
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=128)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "websites"

    @property
    def pages(self):
        return self.pages_set.all()

    def pages_count(self):
        """
        Number of pages belongs.
        :return: int
        """
        return self.pages_set.count()


class WebsitesDBDao(WebsiteDao):
    def find_all(self, offset=0, limit=0):
        query = WebsitesModel.objects.all()
        if limit > 0:
            query = query[:limit]
        if offset > 0:
            query = query[offset:]
        return list(query)

    def persist(self, website):
        if isinstance(website, WebsitesModel):
            website.save()
        else:
            website_model = WebsitesModel()
            WebsitesDBDao._entity_to_model(website, website_model)
            website_model.save()
            website.id = website_model.id

    def save(self, website):
        if isinstance(website, WebsitesModel):
            website.save()
        else:
            website_model = WebsitesModel.objects.get(pk=website.id)
            if not website_model:
                raise RuntimeError()
            WebsitesDBDao._entity_to_model(website, website_model)
            website_model.save()

    def find(self, wid):
        return WebsitesModel.objects.get(pk=wid)

    @classmethod
    def _entity_to_model(cls, entity, model):
        """
        Copies field values from simple entityt to model.
        :param entity: Simple website entity.
        :param model: Website model that extends django's model.
        """
        if (not entity.id is None) and entity.id > 0:
            model.id = entity.id
        model.host = entity.host
        model.name = entity.name
        model.pages = entity.pages

    def delete(self, wid):
        website = WebsitesModel.objects.get(pk=wid)
        if not website:
            raise ValueError("Website with id = %d not found" % wid)
        website.delete()


class PageModel(models.Model, Page):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255, unique=True)
    website = models.ForeignKey(WebsitesModel, related_name='pages_set', on_delete=models.CASCADE)

    def __str__(self):
        return self.url

    class Meta:
        db_table = "pages"


class PagesDBDao(PageDao):
    def find(self, pid):
        return PageModel.objects.get(pk=pid)

    @classmethod
    def _entity_to_model(cls, entity, model):
        """
        Copies field values from simple entity to model.
        :param entity: Simple page entity.
        :param model: Page model that extends django's model.
        """
        if (not entity.id is None) and entity.id > 0:
            model.id = entity.id
        model.url = entity.url
        model.website = entity.website

    def persist(self, page):
        if not isinstance(page, PageModel):
            page_model = PageModel()
            PagesDBDao._entity_to_model(page, page_model)
            page_model.save()
            page.id = page_model.id
        else:
            page.save()

    def save(self, page):
        if not isinstance(page, PageModel):
            page_model = PageModel()
            PagesDBDao._entity_to_model(page, page_model)
            page_model.save()
        else:
            page.save()

    def delete(self, page):
        page_model = PageModel.objects.get(pk=page)
        if page_model:
            page_model.delete()
        else:
            raise ValueError("Page with ID %d not found" % page)

    def find_by_url(self, url):
        try:
            page = PageModel.objects.get(url=url)
        except PageModel.DoesNotExist:
            page = None
        return page


class LoadingModel(models.Model, Loading):
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(PageModel, related_name='loadings_set', on_delete=models.CASCADE)
    success = models.BooleanField(default=False)
    headers = {}
    headers_serialized = models.CharField(max_length=4096)
    content = models.CharField(max_length=1024000)
    time = models.DateTimeField(auto_now=True)
    loading_time = models.PositiveIntegerField()

    def __str__(self):
        return self.content

    class Meta:
        db_table = "loadings"


class LoadingDBDao(LoadingDao):
    @classmethod
    def _entity_to_model(cls, entity, model):
        """
        Copy attributes from entity to django's model.

        :param entity: Loading entity.
        :param model: LoadingModel instance.
        """
        if entity.id > 0:
            model.id = entity.id
        page = entity.page
        if (not isinstance(page, PageModel)) and page.id > 0:
            page = PageModel.objects.get(pk=page.id)
        model.page = page
        model.success = entity.success
        model.headers = entity.headers
        model.headers_serialized = json.dumps(entity.headers)
        model.content = entity.content
        model.time = entity.time
        model.loading_time = entity.loading_time

    def persist(self, loading):
        if isinstance(loading, Loading):
            loading_model = LoadingModel()
            LoadingDBDao._entity_to_model(loading, loading_model)
            loading_model.save()
            loading.id = loading_model.id
        elif isinstance(loading, LoadingModel):
            loading.save()
        else:
            raise ValueError()

    def save(self, loading):
        if isinstance(loading, Loading):
            loading_model = LoadingModel()
            LoadingDBDao._entity_to_model(loading, loading_model)
            loading_model.save()
        elif isinstance(loading, LoadingModel):
            loading.save()
        else:
            raise ValueError()

    def find_all(self, limit=0, offset=0, order_by='time', order_asc=False):
        """
        Gets list of Loadings from storage.
        :param limit: Max amount of entities to return.
        :param offset: Start index.
        :param order_by: Order loadings by property, time or id.
        :param order_asc: True for ascending, false for descending ordering.
        :return: List of Loadings.
        """
        query = LoadingModel.objects.select_related('page').all()
        if order_by in ('time', 'id'):
            if not order_asc:
                order_by = '-' + order_by
            query = query.order_by(order_by)
        if limit > 0:
            query = query[:limit]
        if offset > 0:
            query = query[offset:]
        return list(query)