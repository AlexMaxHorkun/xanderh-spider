from django.contrib import admin

from xanderhorkunspider.web.websites import models


admin.site.register(models.WebsitesModel)
admin.site.register(models.PageModel)
admin.site.register(models.LoadingModel)