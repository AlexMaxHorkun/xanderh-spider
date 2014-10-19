__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from xanderhorkunspider.models import Website
from django.db import models


class WebsitesModel(models.Model, Website):
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=128)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table="websites"

    def __init__(self, *args, **kwargs):
        super(models.Model, self).__init__(self, args, kwargs)