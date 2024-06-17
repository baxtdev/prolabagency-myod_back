from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import FAQ,Advertisement


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id','question')
    ordering = ('id',)
    search_fields = ('question','answer')


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id','title','get_image')
    ordering = ('id',)
    search_fields = ('title','description')
    list_display_links = ('title',)    


    @admin.display(description="photo")
    def get_image(self, instance):
        if instance.photo_1:
            return mark_safe('<img src="{}" width="200px" />'.format(instance.photo_1.url))
        else:
            return None
