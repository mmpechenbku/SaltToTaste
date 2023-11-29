from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatars/', verbose_name='avatar', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Имя")
    nickname = models.CharField(max_length=100, verbose_name="Никнейм", unique=True)
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    # likes =

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.nickname

    @property
    def get_sum_followers(self):
        return self.followers.count()

    @property
    def get_sum_following(self):
        return self.following.count()

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})


class Subscription(models.Model):
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} подписался на {self.following.username}'

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
