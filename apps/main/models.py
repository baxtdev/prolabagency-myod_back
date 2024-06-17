from django.db import models
from apps.utils.models import TimeStampAbstractModel

from django_resized import ResizedImageField

class FAQ(models.Model):
    question = models.CharField(max_length=555, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"
        ordering = ['order']

    def __str__(self):
        return self.question
    


class Advertisement(TimeStampAbstractModel):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    photo_1 = ResizedImageField(
        upload_to='ads/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото 1"
        )
    photo_2 = ResizedImageField(
        upload_to='ads/', 
        force_format='WEBP', 
        quality=90, 
        verbose_name="Фото 2"
        )
    
    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']

    def __str__(self):
        return self.title    