from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


from apps.utils.models import TimeStampAbstractModel


from django_resized import ResizedImageField

# Create your models here.

class Compositions(models.Model):
    name = models.CharField(
        max_length=255, 
        verbose_name='Название',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Состав')
        verbose_name_plural = _('Составы')

    def __str__(self):
        return self.name



class Product(TimeStampAbstractModel):
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='products',
    )
    name = models.CharField(
        max_length=255, 
        verbose_name='Название',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    order_conditions = models.TextField(
        _("Условия заказа"),
        )
    delivery_text = models.TextField(
        _("Delivery")
        )
    price = models.PositiveBigIntegerField(
        _("Цена"),
        )
    discount = models.PositiveSmallIntegerField(
        _("Скидка"),
        blank=True,
        null=True
        )
    composition = models.ManyToManyField(
        'Compositions',
        related_name='products',
        null=True,
        blank=True
    )
    is_popular = models.BooleanField(
        _("Популярный"),
        default=False,
    )
    is_new = models.BooleanField(
        _("Ноинка"),
        default=True
    )
    raiting = models.PositiveSmallIntegerField(
        _("Рейтинг"),
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'products'
        managed = True
        verbose_name = 'Мёд'
        verbose_name_plural = 'Мёд'
        ordering = ['name','-id']

    def __str__(self):
        return f"{self.name}-{self.owner.email}"    

    @property
    def _price(self):
        if self.discount:
            return self.discount
        return self.price

    @property
    def discount_price(self):
        if self.discount:
            return self.discount
        return None

    @property
    def photo(self):
        photo = self.photos.first()
        if photo:
            return photo.photo.url
        return None

    @property
    def _type(self):
        return "product"

class ProductPhotos(models.Model):
    item = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='photos',
    )
    photo = ResizedImageField(
        upload_to='products/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Фотография Мёда'
        verbose_name_plural = 'Фотографии Мёда'

    def __str__(self):
        if self.item:
            return f"Фото Мёда-{self.item.name}"
        
        return f"Фотография Продукта"



class ProductFavorites(TimeStampAbstractModel):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='product_favorites',
    )
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Избранные Мёды'
        verbose_name_plural = 'Избранные Мёды'
        unique_together = ('product', 'user')
        ordering = ['-id']
        index_together = [
            ['product', 'user'],
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_product_favorites'
            )
        ]
        
        
    def __str__(self) -> str:
        return f"Мёд {self.product.name}-Пользователь {self.user.email}" 