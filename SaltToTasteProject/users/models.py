from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    middlename = models.CharField(max_length=100, verbose_name="Отчество")
    email = models.EmailField(verbose_name='Почтовый адрес', unique=True)
    fullname = models.CharField(max_length=100, verbose_name="ФИО")
    pasport = models.CharField(max_length=100, verbose_name="Серия и номер паспорта", unique=True)
    phone_number = models.CharField(max_length=100, verbose_name="Номер телефона", unique=True)
    status = models.BooleanField(default=False, verbose_name='Подтверждение аккаунта')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.fullname

