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
            websiteModel = WebsitesModel(host=website.host, name=website.name)
            websiteModel.save()
            website.id = websiteModel.id