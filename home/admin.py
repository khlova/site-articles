from django.contrib import admin

from .models import News, MessCont

admin.site.register(MessCont)
admin.site.register(News)