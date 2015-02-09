xanderh-spider
==============

##What it does
  Spider loads a web page, saves content then looks for links to other pages within the same web-site and loads their
contents etc.

##About
  Spider is written as a library, which can be applied with any type of application (desktop, web).
Project is written with Python 3 and uses some third-party frameworks/libraries.
Web interface implemented using Django 1.7.

##How to run it
1. Clone it somewhere
2. Run xanderhorkunspider.tests as you usually run unit tests.
3. Get exceptions about some libraries missing - install them.
4. Install django 1.7+.
5. Rename xanderhorkunspider/web/config/local_settings.py.dist to local_settings.py and change it's content
according to your setup.
6. Run django-manage.py migrate to create DB schema.
7. Run web server with django-manage.py runserver (again, you may not have some libraries install them).
8. Explore web interface:
   * sign up
   * create a website (with host like "www.example.com" and name like "example"
   * add a page to your website (with url like "http://www.example.com")
   * run a spider session - it will go to the page created by you, load it contents and look for other pages within
     the website you created