__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django import shortcuts

from xanderhorkunspider import domain
from xanderhorkunspider import dao
from xanderhorkunspider.web.websites import models


def index_view(request):
    """
    Home page of "websites" module.
    :param request: http.HttpRequest.
    :return: http.HttpResponse.
    """
    websites_domain = domain.Websites(dao.PageDao(), models.WebsitesDBDao(), dao.LoadingDao())
    websites = websites_domain.find_websites()
    return shortcuts.render_to_response('websites/index.html', {'websites': websites})