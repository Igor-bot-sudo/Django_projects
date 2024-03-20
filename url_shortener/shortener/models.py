from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from url_shortener.settings import BASE_DIR


class ShortenerURLModel(models.Model):
    hint = models.CharField(max_length=50, verbose_name='Тема')
    long_link = models.CharField(max_length=255, verbose_name='Длинный URL')
    short_link = models.CharField(max_length=255, verbose_name='Короткий URL', default='', unique=True, blank=True)
    qr_code = models.ImageField(upload_to=f'{BASE_DIR}/media', null=True, blank=True, verbose_name='QR-код')
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
