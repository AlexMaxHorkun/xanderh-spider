__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

import json
import base64

from django import shortcuts
from django import http

from xanderhorkunspider.web.websites import models
from xanderhorkunspider.web.websites import forms
from xanderhorkunspider.web.websites import domain


def index_view(request):
    """
    Home page of "websites" module.
    :param request: http.HttpRequest.
    :return: http.HttpResponse.
    """
    websites_domain = domain.websites_domain
    websites = websites_domain.find_websites()
    return shortcuts.render_to_response('websites/index.html', {'websites': websites})


def edit_website_view(request, wid=None):
    template = 'websites/add_website.html'
    websites = domain.websites_domain  # domain.Websites(dao.PageDao(), models.WebsitesDBDao(), dao.LoadingDao())
    website = None
    if not wid is None:
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


def delete_website_view(request, wid=None):
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


def edit_page_view(request, pid=None, wid=None):
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


def delete_page_view(request, pid):
    websites = domain.websites_domain
    page = websites.find_page(pid)
    if not page:
        raise http.Http404()
    if request.method == 'POST':
        websites.remove_page(page)
        return shortcuts.redirect(shortcuts.resolve_url('index'))
    else:
        return shortcuts.render(request, 'websites/delete_page.html', {'page': page})


def spider_session_view(request, wid):
    websites = domain.websites_domain
    website = websites.find(wid)
    if not website:
        raise http.Http404()
    return shortcuts.render(request, 'websites/spider_session.html', {'website': website})


def start_spider_session_view(request):
    wid = request.GET.get('website')
    max_processes = int(request.GET.get('max_processes'))
    if not wid:
        raise http.Http404()
    if max_processes:
        domain.spider_manager.max_process_count = max_processes
    website = domain.websites_domain.find(wid)
    if (not website) or (not len(website.pages)):
        raise http.Http404()
    for p in website.pages:
        domain.spider_manager.crawl(p)
    if not domain.spider_manager.is_alive():
        domain.spider_manager.start()
    return shortcuts.render(request, "websites/start_spider_session.html",
                            {'spider': domain.spider_manager, 'website': website})


def spider_status_view(request):
    """
    Gets information about spider and it's processes. Returns json.
    """
    running_pages = domain.spider_manager.get_active_pages()
    waiting_pages = domain.spider_manager.get_waiting_pages()
    finished_pages = list()
    for crawling_result in domain.spider_manager.crawling_results:
        finished_pages.append(crawling_result.page)
    response_data = {'is_alive': domain.spider_manager.is_alive(), 'running': list(), 'finished': list(),
                     'waiting': list()}
    for p in running_pages:
        response_data['running'].append({
            'url': p.url,
            'website': {'name': p.website.name},
            'id': str(base64.urlsafe_b64encode(str.encode(p.url)))
        })
    for p in waiting_pages:
        response_data['waiting'].append({
            'url': p.url,
            'website': {'name': p.website.name},
            'id': str(base64.urlsafe_b64encode(str.encode(p.url)))
        })
    for p in finished_pages:
        response_data['finished'].append({
            'url': p.url,
            'website': {'name': p.website.name},
            'id': str(base64.urlsafe_b64encode(str.encode(p.url)))
        })
    return http.HttpResponse(json.dumps(response_data), content_type="application/json")