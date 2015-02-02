__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django import shortcuts
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from xanderhorkunspider.web.websites.domain import users
from xanderhorkunspider.web.websites import forms


# Auth related views

def signup_view(request):
    """
    This page allows user to register, contains sign up form.
    :param request: HTTP request.
    :type request: django.http.HttpRequest
    :return: HTTP response.
    :rtype: django.http.HttpResponse
    """
    if request.user.is_authenticated():
        return shortcuts.redirect('index')
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = None
            try:
                user = users.create(form.cleaned_data['username'], email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
            except ValueError:
                # User already exists
                form.add_error("username", "User with such email/username already exists")
            if user:
                user = users.authenticate(username=form.cleaned_data['username'],
                                          password=form.cleaned_data['password'])
                if user:
                    login(request, user)
                    if not form.cleaned_data['rememberme']:
                        request.session.set_expiry(0)
                    return shortcuts.redirect('index')
                else:
                    raise RuntimeError("Unable to create user or authenticate")
    else:
        form = forms.SignupForm()
    return shortcuts.render(request, "websites/auth/signup.html", {'form': form})


@login_required()
def logout_view(request):
    """
    This page allows user to logout, does not contain any HTML output.
    :param request: HTTP request.
    :type request: django.http.HttpRequest
    :return: HTTP response.
    :rtype: django.http.HttpResponse
    """
    if request.user.is_authenticated:
        logout(request)
    return shortcuts.redirect('index')


def login_view(request):
    """
    This page allows user to login, contains login form.
    :param request: HTTP request.
    :type request: django.http.HttpRequest
    :return: HTTP response.
    :rtype: django.http.HttpResponse
    """
    if request.user.is_authenticated():
        return shortcuts.redirect('index')
    bad_credentials_error = False
    if request.method == 'POST':
        if not ('username' in request.POST and 'password' in request.POST):
            bad_credentials_error = True
        else:
            user = users.authenticate(request.POST['username'], request.POST['password'])
            if user:
                login(request, user)
                if not request.POST.get('rememberme', None):
                    request.session.set_expiry(0)
                return shortcuts.redirect('index')
            else:
                bad_credentials_error = True
    return shortcuts.render(request, "websites/auth/login.html", {'bad_credentials': bad_credentials_error})