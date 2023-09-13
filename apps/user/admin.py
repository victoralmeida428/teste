from django.contrib import admin
from .models import PixImage
# Register your models here.
class PixView(admin.ModelAdmin):
    list_display = ('pix', 'valor')
    list_display_links = ('pix', 'valor')

admin.site.register(PixImage, PixView)