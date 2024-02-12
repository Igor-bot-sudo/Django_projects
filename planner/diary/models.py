from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Todo(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема:')
    details = models.TextField(verbose_name='Содержание:')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата / Время:')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title
