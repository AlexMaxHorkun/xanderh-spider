__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

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
            websiteModel = WebsitesModel()
            WebsitesDBDao._entity_to_model(website, websiteModel)
            websiteModel.save()
            website.id = websiteModel.id

    def save(self, website):
        if isinstance(website, WebsitesModel):
            website.save()
        else:
            websiteModel = WebsitesModel.objects.get(pk=website.id)
            if not websiteModel:
                raise RuntimeError()
            WebsitesDBDao._entity_to_model(website, websiteModel)
            websiteModel.save()

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
    url = models.CharField(max_length=255)
    website = models.ForeignKey(WebsitesModel, related_name='pages_set')

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
            pageModel = PageModel()
            PagesDBDao._entity_to_model(page, pageModel)
            pageModel.save()
            page.id = pageModel.id
        else:
            page.save()

    def save(self, page):
        if not isinstance(page, PageModel):
            pageModel = PageModel()
            PagesDBDao._entity_to_model(page, pageModel)
            pageModel.save()
        else:
            page.save()

    def delete(self, page):
        pageModel = PageModel.objects.get(pk=page)
        if pageModel:
            pageModel.delete()
        else:
            raise ValueError("Page with ID %d not found" % page)


class LoadingModel(models.Model, Loading):
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(PageModel, related_name='loadings_set')
    success = models.BooleanField(default=False)
    headers = {}
    headers_serialized = models.CharField(max_length=512)
    content = models.CharField(max_length=8320)
    time = models.DateTimeField(auto_now=True)
    loading_time = models.PositiveIntegerField()

    def __str__(self):
        return self.content

    class Meta:
        db_table = "loadings"


class LoadingDBDao(LoadingDao):
    pass