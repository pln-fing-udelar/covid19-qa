from django.contrib import admin

from .models import QueryConf


@admin.register(QueryConf)
class QueryConfAdmin(admin.ModelAdmin):
    pass
