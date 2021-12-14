# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from main.models import WebsiteUser
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

admin.site.register(WebsiteUser, UserAdmin)
# admin.site.register(FlatPage, FlatPageAdmin)
