from django.contrib import admin

# Register your models here.

from .models import StuffAdmin
from .models import Stuff

admin.site.register(Stuff,StuffAdmin)
