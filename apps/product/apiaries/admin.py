from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import Apiaries,ApiariesPhotos,BookedDays,ApiariesFavorites
# Register your models here.



class PhotosInlie(admin.TabularInline):
    model = ApiariesPhotos
    extra = 0


class BookedDayInline(admin.TabularInline):
    model = BookedDays
    extra = 0    


@admin.register(Apiaries)
class ApiariesAdmin(admin.ModelAdmin):
    list_display = ('name','description','price','discount','get_image')
    ordering = ('name','price','discount')
    search_fields = ('name','description')
    list_filter = ('is_new','is_popular')

    inlines = [PhotosInlie,BookedDayInline]

    @admin.display(description="фото")
    def get_image(self, instance):
        if instance.photo:
            return mark_safe('<img src="{}" width="100px" />'.format(instance.photo))
        else:
            return None


@admin.register(ApiariesPhotos)
class ApiariesPhotosAdmin(admin.ModelAdmin):
    list_display = ('item','get_image')
    search_fields = ('item__name',)


    @admin.display(description="фото")
    def get_image(self, instance):
        if instance.photo:
            return mark_safe('<img src="{}" width="100px" />'.format(instance.photo.url))
        else:
            return None


@admin.register(BookedDays)
class BookedDaysAdmin(admin.ModelAdmin):
    list_display = ('apiaries','start_day','end_day','get_image')
    search_fields = ('apiaries__name',)

    @admin.display(description="Фото Пасеки")
    def get_image(self, instance):
        if instance.apiaries.photo:
            return mark_safe('<img src="{}" width="100px" />'.format(instance.apiaries.photo))
        else:
            return None
    

@admin.register(ApiariesFavorites)
class ApiariesFavoritesAdmin(admin.ModelAdmin):
    list_display = ('user','apiaries','get_image')
    search_fields = ('user__email','apiaries__name','user__first_name')
    ordering = ('-id',)


    @admin.display(description="Фото Пользователя")
    def get_image(self, instance):
        if instance.user.image:
            return mark_safe('<img src="{}" width="100px" />'.format(instance.user.imag.url))
        else:
            return None