from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatars/', verbose_name='avatar', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Имя")
    nickname = models.CharField(max_length=100, verbose_name="Никнейм", unique=True)
    email = models.EmailField(verbose_name='Электронная почта', unique=True)

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.nickname

