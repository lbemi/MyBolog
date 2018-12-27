from django.contrib import admin
from blog.models import *

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','pub_time')

admin.site.register((Category,Comment,Tag))