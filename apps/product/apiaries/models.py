from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


from apps.utils.models import TimeStampAbstractModel


from django_resized import ResizedImageField
# Create your models here.

class Apiaries(TimeStampAbstractModel):
    DAY="day"
    WEEK="week"
    MONTH="month"
    TYPE_PRICE = (
        (DAY,"День"),
        (WEEK,"Неделя"),
        (MONTH,"Месяц")
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='apiaries',
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
    price_for = models.CharField(
        _("Цена за"),
        max_length=10,
        choices=TYPE_PRICE,
        default=DAY
    )    
    price = models.PositiveBigIntegerField(
        _("Цена"),
        )
    discount = models.PositiveSmallIntegerField(
        _("Скидка"),
        blank=True,
        null=True
        )
    location = models.CharField(
        _("Местоположение"),
        max_length=300,
    )
    latitude =  models.CharField(
        _('Широта'),
        help_text = 'Укажите северную широту',
        max_length=50
        )    
    longitude = models.CharField(
        _('Долгота'),
        help_text = 'Укажите восточную долготу',
        max_length=50
        )
    radius = models.CharField(
        _('Радиус'),
        help_text = 'Укажите радиус',
        max_length=50
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
        verbose_name = _("Пасеки")
        verbose_name_plural = _("Пасеки")  
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
        return "apaires"
    



class BookedDays(TimeStampAbstractModel):
    apiaries = models.ForeignKey(
        'Apiaries',
        on_delete=models.CASCADE,
        related_name='booked_days',
        verbose_name=_("Пасеки")
    )
    start_day = models.DateTimeField(
        _("Начало"),
        blank=True,
        null=True
    )     
    end_day = models.DateTimeField(
        _("Конец"),
        blank=True,
        null=True
    )  

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Забронированные дни'
        verbose_name_plural = 'Забронированные дни'

    def clean(self):
        super().clean()
        if self.start_day and self.end_day:
            if self.start_day > self.end_day:
                raise ValidationError("Дата начала не может быть больше даты окончания")
        
            # intersecting_days = self.apiaries.booked_days.exclude(pk=self.pk).filter(
            #     start_day__lte=self.end_day,
            #     end_day__gte=self.start_day,
            # )
            # if intersecting_days.exists():
            #     raise ValidationError("Указанный диапазон дат пересекается с другими забронированными днями")


    def __str__(self) -> str:
        return f"{self.apiaries.name}" 



class ApiariesPhotos(models.Model):
    item = models.ForeignKey(
        'Apiaries',
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_("Пасеки")
    )
    photo = ResizedImageField(
        upload_to='apiaries/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото",
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Фотография Пасеков'
        verbose_name_plural = 'Фотографии Пасеков'

    def __str__(self):
        return self.item.name


class ApiariesFavorites(TimeStampAbstractModel):
    apiaries = models.ForeignKey(
        'Apiaries',
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_("Пасеки")
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='apiaries_favorites',
    )
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Избранные Пасеки'
        verbose_name_plural = 'Избранные Пасеки'
        unique_together = ('apiaries', 'user')
        ordering = ['-id']
        index_together = [
            ['apiaries', 'user'],
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['apiaries', 'user'],
                name='unique_apiaries_favorites'
            )
        ]
        
        
    def __str__(self) -> str:
        return f"Пасеки {self.apiaries.name}-Пользователь {self.user.email}"
    
  
        