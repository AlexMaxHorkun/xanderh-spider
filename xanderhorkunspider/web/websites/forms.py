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


class SignupForm(forms.Form):
    username = forms.CharField(max_length=256, min_length=3, required=True)
    email = forms.EmailField(max_length=512, min_length=5, required=True)
    password = forms.CharField(max_length=64, min_length=7, widget=forms.PasswordInput, required=True)
    rememberme = forms.BooleanField(initial=True, required=False)