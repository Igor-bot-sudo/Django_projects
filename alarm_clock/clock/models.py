from django.db import models
from django.contrib.auth.models import User


class AlarmClockModel(models.Model):
    hint = models.CharField(max_length=50, verbose_name='Заголовок')
    alarm_time = models.CharField(max_length=5, verbose_name='Время', unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
