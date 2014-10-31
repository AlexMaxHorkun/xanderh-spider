__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django.db import models

from xanderhorkunspider.models import Website
from xanderhorkunspider.dao import WebsiteDao


class WebsitesModel(models.Model, Website):
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=128)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "websites"


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

    def delete(self, wid):
        website = WebsitesModel.objects.get(pk=wid)
        if not website:
            raise ValueError("Website with id = %d not found" % wid)
        website.delete()