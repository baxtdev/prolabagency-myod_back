from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import Order,OrderApiaries,OrderProducts,OrderEqipments,ItemReviews
# Register your models here.



class OrderApiariesInlie(admin.TabularInline):
    model = OrderApiaries
    extra = 0


class OrderProductsInline(admin.TabularInline):
    model = OrderProducts
    extra = 0    


class OrderEqipmentsInline(admin.TabularInline):
    model = OrderEqipments
    extra = 0  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name','adress','owner','get_image','code_number')
    inlines = [OrderApiariesInlie,OrderProductsInline,OrderEqipmentsInline]
    search_fields = ('name','adress','code_number','owner__first_name','owner__last_name')
    ordering = ('-id',)
    list_filter = ('items__status',)
    @admin.display(description="Фото Пользователя")
    def get_image(self, instance):
        if instance.owner:
            owner = instance.owner
            if owner.image:
                return mark_safe('<img src="{}" width="100px" />'.format(instance.owner.image.url))
        else:
            return None


class CatalogOrderAdmin(admin.ModelAdmin):
    list_display = ('order','item','quantity','status')
    list_filter = ('status',)
    search_fields = ('order__name','item__name','order__owner__first_name','order__owner__last_name')
    ordering = ('-id',)


@admin.register(OrderApiaries)
class OrderApiariesAdmin(CatalogOrderAdmin):
    pass
    


@admin.register(OrderProducts)
class OrderProductssAdmin(CatalogOrderAdmin):
    pass



@admin.register(OrderEqipments)
class OrderEqipmentsAdmin(CatalogOrderAdmin):
    pass



@admin.register(ItemReviews)
class ItemReviewsAdmin(admin.ModelAdmin):
    list_display = ('owner','mark','comment')
    search_fields = ('owner__first_name','owner__last_name','comment')
    list_filter = ('mark',)