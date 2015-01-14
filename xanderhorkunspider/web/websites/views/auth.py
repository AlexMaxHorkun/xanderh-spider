__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'

from django import shortcuts
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from xanderhorkunspider.web.websites import forms


# Auth related views

def signup_view(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            User.objects.create_user(form.cleaned_data['username'], email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password'])
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return shortcuts.redirect('index')
            else:
                raise RuntimeError("Unable to create user or authenticate")
    else:
        form = forms.SignupForm()
    return shortcuts.render(request, "websites/auth/signup.html", {'form': form})