__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django import shortcuts

from xanderhorkunspider import domain
from xanderhorkunspider import dao
from xanderhorkunspider.web.websites import models
from xanderhorkunspider.web.websites import forms


def index_view(request):
    """
    Home page of "websites" module.
    :param request: http.HttpRequest.
    :return: http.HttpResponse.
    """
    websites_domain = domain.Websites(dao.PageDao(), models.WebsitesDBDao(), dao.LoadingDao())
    websites = websites_domain.find_websites()
    return shortcuts.render_to_response('websites/index.html', {'websites': websites})


def add_website_view(request):
    template = 'websites/add_website.html';
    websites = domain.Websites(dao.PageDao(), models.WebsitesDBDao(), dao.LoadingDao());
    if request.method == 'POST':
        form = forms.WebsiteForm(request.POST)
        if form.is_valid():
            website = models.WebsitesModel()
            website.host = form.cleaned_data['host'];
            website.name = form.cleaned_data['name'];
            websites.persist(website)
            return shortcuts.redirect('/')
    else:
        form = forms.WebsiteForm()
    return shortcuts.render(request, template, {'form': form});