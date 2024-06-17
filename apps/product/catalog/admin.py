from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import Product,Compositions,ProductPhotos,ProductFavorites
# Register your models here.



class PhotosInlie(admin.TabularInline):
    model = ProductPhotos
    extra = 0



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description','price','discount','get_image')
    ordering = ('name','price','discount')
    search_fields = ('name','description')
    list_filter = ('is_new','is_popular')

    inlines = [PhotosInlie]

    @admin.display(description="фото")
    def get_image(self, instance):
        if instance.photo:
            return mark_safe('<img src="{}" width="100px" />'.format(instance.photo))
        else:
            return None


@admin.register(Compositions)
class CompositionsAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ('name','description')
    ordering = ('name','-id')



@admin.register(ProductPhotos)
class ProductPhotosAdmin(admin.ModelAdmin):
    list_display = ('item','get_image')
    search_fields = ('item__name',)


    @admin.display(description="фото")
    def get_image(self, instance):
        if instance.photo:
            return mark_safe('<img src="{}" width="100px" />'.format(instance.photo.url))
        else:
            return None


@admin.register(ProductFavorites)
class ProductFavoritesAdmin(admin.ModelAdmin):
    list_display = ('user','product','get_image')
    search_fields = ('user__email','product__name','user__first_name')
    ordering = ('-id',)


    @admin.display(description="Фото Пользователя")
    def get_image(self, instance):
        if instance.user.image:
            return mark_safe('<img src="{}" width="100px" />'.format(instance.user.imag.url))
        else:
            return None