from django.urls import path, include
from django.contrib.auth.views import LoginView

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/login/', 
        LoginView.as_view(
            template_name='admin/login.html',
            extra_context={         
              'title': 'Login',
              'site_title': 'My Site',
              'site_header': 'Login'}
        ),
    name='login'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path("", hello.views.StuffListView.as_view(extra_context={         
              'title': 'Stuffs',
              'site_title': 'My Site',
              'site_header': 'Stuffs',
        }), name="clist"),
    path("test",hello.views.StuffTableView.as_view(extra_context={         
              'title': 'Stuffs',
              'site_title': 'My Site',
              'site_header': 'Stuffs',
        }), name="test"),
    path("unrz/<unrz>", hello.views.unrz, name="unrz"),
    path("cert/<cert>", hello.views.cert, name="cert"),
    path('hello/', include('hello.urls')),
]
