__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django.conf.urls import patterns, url

from xanderhorkunspider.web.websites import views


urlpatterns = patterns('',
                       url(r'^$', views.index_view, name='index'),
)