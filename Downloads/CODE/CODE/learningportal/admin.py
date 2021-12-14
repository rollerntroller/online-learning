from django.contrib import admin

# Register your models here.
from .models import Content, WatchListItem, Contact


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'video',
        'user',
    )
    list_filter = ('user',)
    search_fields = ('slug', 'title')
    autocomplete_fields = ('user',)


@admin.register(WatchListItem)
class WatchListItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'date_created')
    list_filter = ('user', 'content', 'date_created')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'date_created',
    )
    list_filter = ('date_created',)
    search_fields = ('name',)


