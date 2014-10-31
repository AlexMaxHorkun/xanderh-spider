__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django.conf.urls import patterns, url

from xanderhorkunspider.web.websites import views


urlpatterns = patterns('',
                       url(r'^$', views.index_view, name='index'),
                       url(r'^add-website$', views.edit_website_view, name='add_website'),
                       url(r'^edit-website/(?P<wid>\d+)$', views.edit_website_view, name='edit_website'),
                       url(r'^delete_website/(?P<wid>\d+)$', views.delete_website_view, name='delete_website')
)