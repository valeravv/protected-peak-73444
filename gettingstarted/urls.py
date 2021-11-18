from django.urls import path, include

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
    path("list/", hello.views.StuffListView.as_view(), name="clist"),
    path("unrz/<unrz>", hello.views.unrz, name="unrz"),
    path("cert/<cert>", hello.views.cert, name="cert"),
    path('hello/', include('hello.urls')),
]
