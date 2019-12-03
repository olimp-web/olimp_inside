from django.contrib import admin

from .models import Article, Tag

# Register your models here.


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'label')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('url', 'creator')
