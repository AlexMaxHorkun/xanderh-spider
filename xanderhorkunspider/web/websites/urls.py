__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django.conf.urls import patterns, url

from xanderhorkunspider.web.websites.views import websites, auth


urlpatterns = patterns('',
                       url(r'^$', websites.index_view, name='index'),
                       url(r'^add-website$', websites.edit_website_view, name='add_website'),
                       url(r'^edit-website/(?P<wid>\d+)$', websites.edit_website_view, name='edit_website'),
                       url(r'^delete_website/(?P<wid>\d+)$', websites.delete_website_view, name='delete_website'),
                       url(r'^add-page', websites.edit_page_view, name='add_page'),
                       url(r'^website/(?P<wid>\d+)/add-page', websites.edit_page_view, name='add_page_to_website'),
                       url(r'^edit-page/(?P<pid>\d+)', websites.edit_page_view, name='edit_page'),
                       url(r'^delete_page/(\d+)$', websites.delete_page_view, name='delete_page'),
                       url(r'^spider_session/webiste-(?P<wid>\d+)$', websites.spider_session_view,
                           name='spider_session'),
                       url(r'^spider_session$', websites.start_spider_session_view, name='start_spider_session'),
                       url(r'^spider-status/(.+)$', websites.spider_status_view, name='spider_status'),
                       url(r'^sign-up$', auth.signup_view, name='signup'),
                       url('logout', auth.logout_view, name='logout'),
                       url('login', auth.login_view, name='login'),
)