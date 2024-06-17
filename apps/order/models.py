from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

from apps.utils.models import TimeStampAbstractModel
from apps.utils.fields import UniqueBigIntegerField
IN_BROWSING = "in browsing"
IN_PROCESSING = "in processing"
DONE = "Done"
REJECT = "Reject"

STATUS_CHOICE = (
    (IN_BROWSING,"в просмотре"),
    (IN_PROCESSING,"в процессе"),
    (DONE,"Получено"),
    (REJECT,"ОТКЛОНЕН")
)


class Order(TimeStampAbstractModel):
    code_number = UniqueBigIntegerField(
        _("Номер заказа"),
        unique=True,
        blank=True, 
        null=True
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
        blank=True,
        verbose_name=_("Пользователь")
    )
    name = models.CharField(
        _("ФИО"),
        max_length=300
        )
    email = models.EmailField(
        _("Эл.почта"), 
        max_length=254,
    )
    phone = PhoneNumberField(
        'Телефон',
        blank=True, 
        null=True
        )
    adress = models.CharField(
        _("Адресс"), 
        max_length=300,
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return f"{self.name}-{self.adress}"
    
    @property
    def number(self):
        if self.code_number:
            return self.code_number
        return self.id
    
    @property
    def total(self):
        items = [x.item_total for x in self.items.all()]
        equipments = [a.item_total for a in self.equipments.all()]
        apiaries = [e.item_total for e in self.equipments.all()]
        return sum([sum(items),sum(equipments),sum(apiaries)])


class OrderProducts(TimeStampAbstractModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )
    item = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        related_name='orders',
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name='Кол-во',
        default=1
    )
    status = models.CharField(
        max_length=30,
        choices = STATUS_CHOICE,
        default = IN_BROWSING,
    )

    class Meta:
        verbose_name = _("Товары заказа Мед")
        verbose_name_plural = _("Товары заказа Мед")
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.order.name}-{self.item.name}" 

    @property
    def item_total(self):
        return self.item._price * self.quantity



class OrderEqipments(TimeStampAbstractModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='equipments',
    )
    item = models.ForeignKey(
        'equipments.Equipment',
        on_delete=models.CASCADE,
        related_name='orders',
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name='Кол-во',
        default=1
    )
    status = models.CharField(
        max_length=30,
        choices = STATUS_CHOICE,
        default = IN_BROWSING,
    )

    class Meta:
        verbose_name = _("Товары заказа Оборудование")
        verbose_name_plural = _("Товары заказа Оборудование")
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.order.name}-{self.item.name}"    
    
    @property
    def item_total(self):
        return self.item._price * self.quantity


class OrderApiaries(TimeStampAbstractModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='apiaries',
    )
    item = models.ForeignKey(
        'apiaries.Apiaries',
        on_delete=models.CASCADE,
        related_name='orders',
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name='Кол-во',
        default=1
    )
    status = models.CharField(
        max_length=30,
        choices = STATUS_CHOICE,
        default = IN_BROWSING,
    )
    start_date = models.DateTimeField(
        verbose_name='Дата начала',
        blank=True,
        null=True
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания',
        blank=True,
        null=True
    )

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Товары Заказа Пасеки'
        verbose_name_plural = 'Товары Заказа Пасеки'

    def __str__(self) -> str:
        return f"{self.order.name}-{self.item.name}"    

    @property
    def item_total(self):
        return self.item._price * self.quantity

    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("Дата начала не может быть больше даты окончания")

            intersecting_days = self.item.booked_days.filter(
                start_day__lte=self.start_date,
                end_day__gte=self.end_date,
            )
            if intersecting_days.exists():
                raise ValidationError("Указанный диапазон дат пересекается с забронированными днями")



class ItemReviews(TimeStampAbstractModel):
    mark = models.PositiveSmallIntegerField(
        _("Оценка"),
        default=1
        )
    comment = models.TextField(
        _("Комментарий"),
        blank=True,
        null=True
        )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.SET_NULL,
        related_name='reviews',
        null=True,
        blank=True
    )
    equipments = models.ForeignKey(
        'apiaries.Apiaries',
        on_delete=models.SET_NULL,
        related_name='reviews',
        null=True,
        blank=True
    )
    apiaries = models.ForeignKey(
        'equipments.Equipment',
        on_delete=models.SET_NULL,
        related_name='reviews',
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        "users.User", 
        verbose_name=_("Пользовател"), 
        on_delete=models.CASCADE,
        related_name="reviews"
        )
    
    class Meta:
        verbose_name = _("Коментарие")
        verbose_name_plural = _("Коментарии")


    def __str__(self) -> str:
        return f"{self.mark}-{self.owner}"    

