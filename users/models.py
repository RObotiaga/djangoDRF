from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='почта', unique=True)
    phone = models.CharField(max_length=20, verbose_name='номер')
    city = models.CharField(max_length=20, verbose_name='город', blank=True)
    avatar = models.ImageField(upload_to='avatar/', verbose_name='аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
