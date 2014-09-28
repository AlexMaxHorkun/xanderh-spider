__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

import unittest
import httpretty
from xanderhorkunspider import loader


class TestLoader(unittest.TestCase):
    mock_url = "http://www.example.com/"
    mock_content = "<html><head><title>Some title</title></head><body><h1>Hello you!</h1></body></html>"
    mock_contenttype = "text/html"
    mock_headers = {'age': '19'}

    @httpretty.activate
    def test_load(self):
        httpretty.register_uri(httpretty.GET, self.mock_url,
                               body=self.mock_content,ccontent_type=self.mock_contenttype,
                               adding_headers=self.mock_headers)
        l=loader.Loader(2)
        response=l.load(self.mock_url)
        self.assertIsInstance(response, loader.LoadResult, "Loader did not return LoadResult")
        for key, value in self.mock_headers.items():
            self.assertTrue(key in response.headers, "Response does not contain needed header")
            self.assertTrue(response.headers[key] == value, "Response header's '%s' value is invalid" % key)
        self.assertTrue(response.url == self.mock_url)
        self.assertTrue(response.body == self.mock_content)