from django.contrib import admin

# Register your models here.

from .models import Greeting, StuffAdmin
from .models import Stuff

admin.site.register(Greeting)
admin.site.register(Stuff,StuffAdmin)
