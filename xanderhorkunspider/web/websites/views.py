__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django import shortcuts

from xanderhorkunspider.web.websites import models


def index_view(request):
    """
    Home page of "websites" module.
    :param request: http.HttpRequest.
    :return: http.HttpResponse.
    """
    websites = list(models.WebsitesModel.objects.all())
    return shortcuts.render_to_response('websites/index.html', {'websites': websites})