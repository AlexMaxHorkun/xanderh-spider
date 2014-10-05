__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

import unittest
import sys

import httpretty

from xanderhorkunspider import loader
from xanderhorkunspider import models
from xanderhorkunspider import parser
from xanderhorkunspider import spider
from xanderhorkunspider import domain


class TestLoader(unittest.TestCase):
    mock_url = "http://www.example.com/"
    mock_content = "<html><head><title>Some title</title></head><body><h1>Hello you!</h1></body></html>"
    mock_contenttype = "text/html"
    mock_headers = {'age': '19'}

    @httpretty.activate
    def test_load(self):
        httpretty.register_uri(httpretty.GET, self.mock_url,
                               body=self.mock_content, ccontent_type=self.mock_contenttype,
                               adding_headers=self.mock_headers)
        l = loader.Loader(2)
        response = l.load(self.mock_url)
        self.assertIsInstance(response, loader.LoadResult, "Loader did not return LoadResult")
        for key, value in self.mock_headers.items():
            self.assertTrue(key in response.headers, "Response does not contain needed header")
            self.assertTrue(response.headers[key] == value, "Response header's '%s' value is invalid" % key)
        self.assertTrue(response.url == self.mock_url)
        self.assertTrue(response.body == self.mock_content)


class TestLinksParser(unittest.TestCase):
    mock_host = "example.com"
    mock_text = "<html><head><title>Some title</title></head><body><h1>Hello you!</h1>" \
                "<a someattr=\"someshit\" href=\"/relative-link/23\" otherattr>AAA</a><p>someshit</p>" \
                "<a href=\"http://ohersubdomain.example.com/someshit\">DDD</a>" \
                "<p>Some text <a dd=\"jdsh\" href=\"http://example.com/gofuckyourself\"></a>" \
                "<a href=\"http://fuckthislink.com/someshit2\">SDaa</a>" \
                "<a hh=\"dsad\" href=\"gofurther\">SSSS</a></p></body></html>"
    mock_page_url = "http://somesubdomain.example.com"
    mock_url = "/someshit"

    def test_parse(self):
        website = models.Website("http://www" + self.mock_host, "Some site", self.mock_host)
        page = models.Page(website, self.mock_page_url + self.mock_url)
        loading = models.Loading(page, True, self.mock_text)
        p = parser.OwnLinksParser()
        links = p.parse(loading)
        testlinks = {self.mock_page_url + '/relative-link/23', 'http://ohersubdomain.example.com/someshit',
                     "http://" + self.mock_host + '/gofuckyourself',
                     self.mock_page_url + self.mock_url + '/gofurther'}
        print(links)
        print(testlinks)
        self.assertTrue(links == testlinks)


class TestSpider(unittest.TestCase):
    mock_host = "example.com"
    mock_url = "http://www." + mock_host
    mock_content = "<html><head><title>Some title</title></head><body><h1>Hello you!</h1>" \
                   "<a href=\"someotherpage\">Some link</a></body></html>"

    @httpretty.activate
    def test_crawl(self):
        httpretty.register_uri(httpretty.GET, self.mock_url,
                               body=self.mock_content)
        website = models.Website(self.mock_url, "Test", self.mock_host)
        page = models.Page(website, self.mock_url)
        spdr = spider.Spider()
        loading, links = spdr.crawl_on_page(page)
        self.assertTrue(isinstance(loading, models.Loading))
        self.assertTrue(loading.success)
        self.assertTrue(loading.content == self.mock_content)
        self.assertTrue(page is loading.page)
        self.assertTrue(links == {self.mock_url + "/someotherpage", })


class MockWebsites(domain.Websites):
    loadings = []

    def __init__(self):
        super().__init__(None, None, None)

    def saveLoading(self, loading):
        self.loadings.append(loading)

    def findPageByUrl(self, url):
        return None

    def createPageFromUrl(self, url):
        websites = models.Website("", "", "")
        page = models.Page(websites, url)
        return page


class TestSpiderManager(unittest.TestCase):
    mock_host = "example.com"
    mock_base_url = "http://somesub." + mock_host + "/somepage"

    @httpretty.activate
    def test_threepages(self):
        """website=models.Website("http://www."+self.mock_host, "some site", self.mock_host)
        page1=models.Page(website,self.mock_base_url)
        page2=models.Page(website, self.mock_base_url+'/page2')
        httpretty.register_uri(httpretty.GET, page1.url,
                               body="<p>somestuff</p>")
        httpretty.register_uri(httpretty.GET, page2.url,
                               body="<p>sup</p><a href=\"page3\">link to 3</a>")
        httpretty.register_uri(httpretty.GET, page2.url+"/page3",
                               body="<div>enough</div>")"""
        websites = MockWebsites()
        website = models.Website("http://www.yandex.ru", "Yandex", "yandex.ru")
        page1 = models.Page(website, "http://www.yandex.ua")
        spdr = spider.Spider(loader.Loader(), parser.OwnLinksParser())
        spider_manager = spider.SpiderManager(websites, spdr)
        spider_manager.crawl(page1)
        # spider_manager.start()
        while True:
            if len(websites.loadings) > 10:
                sys.exit(1)
        """received_links=set()
        for l in websites.loadings:
            received_links.add(l.page.url)
        self.assertTrue(received_links == {self.mock_base_url, self.mock_base_url+'/page2', page2.url+"/page3"})"""