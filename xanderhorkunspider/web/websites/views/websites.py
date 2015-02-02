__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

import json
import base64

from django import shortcuts
from django import http
from django.contrib.auth.decorators import permission_required

from xanderhorkunspider.web.websites import models
from xanderhorkunspider.web.websites import forms
from xanderhorkunspider.web.websites import domain


def index_view(request):
    """
    Home page of "websites" module.
    Shows list of websites and some of their pages along with most recent loadings.

    :type request: django.http.HttpRequest
    :rtype: django.http.HttpResponse
    """
    websites_domain = domain.websites_domain
    websites = websites_domain.find_websites()
    last_loadings = domain.websites_domain.find_last_loadings()
    return shortcuts.render(request, 'websites/index.html', {'websites': websites, 'last_loadings': last_loadings})


@permission_required('websites.edit_websites')
def edit_website_view(request, wid=None):
    """
    Page allows to create/edit a website entity.

    :type request: django.http.HttpRequest
    :param wid: Website's ID, it's an edit form when given, create form otherwise.
    :rtype: django.http.HttpResponse
    """
    template = 'websites/add_website.html'
    websites = domain.websites_domain
    website = None
    if wid is not None:
        website = websites.find(wid)
    if not website:
        website = models.WebsitesModel()
    if request.method == 'POST':
        form = forms.WebsiteForm(request.POST)
        if form.is_valid():
            website.host = form.cleaned_data['host']
            website.name = form.cleaned_data['name']
            if not website.id:
                websites.persist(website)
            else:
                websites.save(website)
            return shortcuts.redirect(shortcuts.resolve_url('index'))
    else:
        form_data = None
        if website.id:
            form_data = dict()
            form_data['name'] = website.name
            form_data['host'] = website.host
        form = forms.WebsiteForm(form_data)
    return shortcuts.render(request, template, {'form': form, 'website': website})


@permission_required('websites.edit_websites')
def delete_website_view(request, wid):
    """
    User can delete a website here.

    :param wid: Website's ID.
    :type request: django.http.HttpRequest
    :rtype: django.http.HttpResponse
    """
    template = 'websites/delete_website.html'
    websites = domain.websites_domain
    website = websites.find(wid)
    if not website:
        raise http.Http404
    if request.method == 'POST':
        websites.remove(website)
        return shortcuts.redirect(shortcuts.resolve_url('index'))
    else:
        return shortcuts.render(request, template, {'website': website})


@permission_required('websites.edit_websites')
def edit_page_view(request, pid=None, wid=None):
    """
    Page allows to create/edit a website's page entity.

    :type request: django.http.HttpRequest
    :param wid: Website's ID, when given the would be able to be assigned only to this website.
    :param pid: Page's ID, if given it's an edit form, create form otherwise.
    :rtype: django.http.HttpResponse
    """
    template = 'websites/edit_page.html'
    websites = domain.websites_domain
    if pid:
        page = websites.find_page(pid)
        if not page:
            raise http.Http404()
    else:
        page = models.PageModel()
    if wid:
        website = websites.find(wid)
        if not website:
            raise http.Http404()
        page.website = website
    if request.method == 'POST':
        form = forms.PageForm(request.POST, instance=page)
        if form.is_valid():
            websites.save_page(page)
            return shortcuts.redirect(shortcuts.resolve_url('index'))
    else:
        form = forms.PageForm(instance=page)
    return shortcuts.render(request, template, {'page': page, 'form': form})


@permission_required('websites.edit_websites')
def delete_page_view(request, pid):
    """
    User can delete a website's page here.

    :param pid: Page's ID.
    :type request: django.http.HttpRequest
    :rtype: django.http.HttpResponse
    """
    websites = domain.websites_domain
    page = websites.find_page(pid)
    if not page:
        raise http.Http404()
    if request.method == 'POST':
        websites.remove_page(page)
        return shortcuts.redirect(shortcuts.resolve_url('index'))
    else:
        return shortcuts.render(request, 'websites/delete_page.html', {'page': page})


@permission_required('websites.run_spider_sessions')
def spider_session_view(request, wid):
    """
    User can start and/or monitor a spider session here.
    Spider loads a website's pages' contents, saves it and finds links to new pages in it.

    :param wid: Website's ID.
    :type request: django.http.HttpRequest
    :rtype: django.http.HttpResponse
    """
    websites = domain.websites_domain
    website = websites.find(wid)
    if not website:
        raise http.Http404()
    if 'spider_id' in request.GET:
        spider_id = int(request.GET['spider_id'])
    else:
        spider_id = 0
    return shortcuts.render(request, 'websites/spider_session.html',
                            {'website': website, 'spider_id': spider_id,
                             'default_max_process_count': domain.spider_factory.max_processes})


@permission_required('websites.run_spider_sessions')
def start_spider_session_view(request):
    """
    This is a block at "spider session" page. It shows current processes and stuff.

    :type request: django.http.HttpRequest
    :rtype: django.http.HttpResponse
    """
    wid = request.GET.get('website')
    sid = request.GET.get('spider_id')
    if request.GET.get('max_processes'):
        max_processes = int(request.GET.get('max_processes'))
    else:
        max_processes = 5
    if not wid:
        raise http.Http404()
    website = domain.websites_domain.find(wid)
    if sid:
        spider = domain.spider_factory.find_spider_by_id(request.GET['spider_id'])
        if not spider:
            raise ValueError("No spider found with ID %s" % request.GET['spider_id'])
    else:
        spider = domain.spider_factory.create_spider()
        if max_processes:
            spider.max_process_count = max_processes
        if (not website) or (not len(website.pages)):
            raise http.Http404()
        for p in website.pages:
            spider.crawl(p)
        if not spider.is_alive():
            spider.start()
    return shortcuts.render(request, "websites/start_spider_session.html",
                            {'spider': spider, 'website': website, 'spider_id': id(spider)})


@permission_required('websites.run_spider_sessions')
def spider_status_view(request, sid):
    """
    Gets information about spider and it's processes. Returns json.

    :type request: django.http.HttpRequest
    :rtype: django.http.HttpResponse
    """
    spider_manager = domain.spider_factory.find_spider_by_id(sid)
    if not spider_manager:
        raise ValueError("No spider with ID '%s' found" % sid)
    info = spider_manager.active_processes_info()
    response_data = {'is_alive': spider_manager.is_alive(), 'loadings': list()}
    for crawling in info:
        crawling_data = {
            'url': crawling.page.url,
            'website': {'name': crawling.page.website.name},
            'id': base64.urlsafe_b64encode(str.encode(crawling.page.url)).decode(),
            'started': crawling.started.strftime("%y,%m,%d,%H,%M,%S")
        }
        response_data['loadings'].append(crawling_data)

    if 'website_id' in request.GET:
        website = domain.websites_domain.find(request.GET['website_id'])
        if website:
            response_data['pages_count'] = website.pages.count()
    if 'stop_when_done' in request.GET:
        if int(request.GET['stop_when_done']) != 0:
            spider_manager.stop_when_done = True
    return http.HttpResponse(json.dumps(response_data), content_type="application/json")