from django.urls import path, include

from . import views 

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", views.index, name="index"),
    path("db/", views.db, name="db"),
    path("unrz/<unrz>", views.unrz, name="unrz"),
    path("cert/<cert>", views.cert, name="cert"),
    path("dump/",views.dump, name="dump"),
    path("dumpin/",views.dumpin, name="dumpin"),
]
