__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django import http


def index(request):
    """
    Home page of "websites" module.
    :param request: http.HttpRequest.
    :return: http.HttpResponse.
    """
    return http.HttpResponse("Testing")