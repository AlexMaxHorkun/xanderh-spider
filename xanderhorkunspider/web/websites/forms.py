__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django import forms

from xanderhorkunspider.web.websites import models


class WebsiteForm(forms.Form):
    host = forms.CharField(max_length=128, min_length=1)
    name = forms.CharField(min_length=2, max_length=128)


class PageForm(forms.ModelForm):
    class Meta:
        model = models.PageModel
        fields = ['url', 'website']