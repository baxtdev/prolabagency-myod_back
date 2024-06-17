from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import Category,Equipment,EquipmentPhotos,EquipmentFavorites
# Register your models here.



class PhotosInlie(admin.TabularInline):
    model = EquipmentPhotos
    extra = 0



@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name','description','price','discount','get_image')
    ordering = ('name','price','discount')
    search_fields = ('name','description')
    inlines = [PhotosInlie]
    list_filter = ('is_new','is_popular')
   
    @admin.display(description="фото")
    def get_image(self, instance):
        if instance.photo:
            return mark_safe('<img src="{}" width="100px" />'.format(instance.photo))
        else:
            return None



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    search_fields = ('name','description')
    ordering = ('name','-id')



@admin.register(EquipmentPhotos)
class EquipmentPhotosPhotosAdmin(admin.ModelAdmin):
    list_display = ('item','get_image')
    search_fields = ('item__name',)



    @admin.display(description="фото")
    def get_image(self, instance):
        if instance.photo:
            return mark_safe('<img src="{}" width="100px" />'.format(instance.photo.url))
        else:
            return None


@admin.register(EquipmentFavorites)
class EquipmentFavoritesAdmin(admin.ModelAdmin):
    list_display = ('user','equipment','get_image')
    search_fields = ('user__email','equipment__name','user__first_name')
    ordering = ('-id',)


    @admin.display(description="Фото Пользователя")
    def get_image(self, instance):
        if instance.user.image:
            return mark_safe('<img src="{}" width="100px" />'.format(instance.user.imag.url))
        else:
            return None