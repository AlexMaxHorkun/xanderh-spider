__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django import shortcuts
from django import http

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


def edit_website_view(request, wid=None):
    template = 'websites/add_website.html';
    websites = domain.Websites(dao.PageDao(), models.WebsitesDBDao(), dao.LoadingDao())
    website = None
    if not wid is None:
        website = websites.find(wid)
    if not website:
        website = models.WebsitesModel()
    if request.method == 'POST':
        form = forms.WebsiteForm(request.POST)
        if form.is_valid():
            website.host = form.cleaned_data['host'];
            website.name = form.cleaned_data['name'];
            if not website.id:
                websites.persist(website)
            else:
                websites.save(website)
            return shortcuts.redirect(shortcuts.resolve_url('index'))
    else:
        formData = None
        if website.id:
            formData = {}
            formData['name'] = website.name
            formData['host'] = website.host
        form = forms.WebsiteForm(formData)
    return shortcuts.render(request, template, {'form': form, 'website': website})


def delete_website_view(request, wid=None):
    template = 'websites/delete_website.html'
    websites = domain.Websites(dao.PageDao(), models.WebsitesDBDao(), dao.LoadingDao())
    website = websites.find(wid)
    if not website:
        raise http.Http404
    if request.method == 'POST':
        websites.remove(website)
        return shortcuts.redirect(shortcuts.resolve_url('index'))
    else:
        return shortcuts.render(request, template, {'website': website})


def edit_page_view(request, pid=None, wid=None):
    template = 'websites/edit_page.html'
    websites = domain.Websites(dao.PageDao(), models.WebsitesDBDao(), dao.LoadingDao())
    website = None
    page = None
    if wid:
        website = websites.find(wid)
    if pid:
        page = websites.find_page(pid)
        if not page:
            raise http.Http404()
    if request.method == 'POST':
        form = forms.PageForm(request.POST, instance=page)
        if form.is_valid():
            websites.save_page(page)
            return shortcuts.redirect(shortcuts.resolve_url('index'))
    else:
        form = forms.PageForm(instance=page)
    return shortcuts.render(request, template, {'website': website, 'form': form})