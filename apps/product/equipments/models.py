from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


from apps.utils.models import TimeStampAbstractModel


from django_resized import ResizedImageField

# Create your models here.
class Category(models.Model):
    name = models.CharField(
        _("Название"),
        max_length=200
    )
    description = models.TextField(
        _("Описание"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['-id','name']

    def __str__(self) -> str:
        return f"{self.name}"



class Equipment(TimeStampAbstractModel):
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='equipments',
        verbose_name=_("Пользовател"),
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name="items",
        verbose_name=_('Категория')
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
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ['-id','name']

    def __str__(self) -> str:
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
        return "equipments"

class EquipmentPhotos(models.Model):
    item = models.ForeignKey(
        'Equipment',
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_("Оборудование")
    )
    photo = ResizedImageField(
        upload_to='equipments/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Фотография Оборудование'
        verbose_name_plural = 'Фотографии Оборудование'

    def __str__(self):
        return self.item.name
    


class EquipmentFavorites(TimeStampAbstractModel):
    equipment = models.ForeignKey(
        'Equipment',
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_("Оборудование")
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='equipment_favorites',
    )
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Избранные Оборудовании'
        verbose_name_plural = 'Избранные Оборудовании'
        unique_together = ('equipment', 'user')
        ordering = ['-id']
        index_together = [
            ['equipment', 'user'],
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['equipment', 'user'],
                name='unique_equipment_favorites'
            )
        ]
        
        
    def __str__(self) -> str:
        return f"Оборудование {self.equipment.name}-Пользователь {self.user.email}"