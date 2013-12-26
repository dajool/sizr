# -*- coding: utf-8 -*-

from django.contrib import admin
from image_sizr.models import Image

class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)