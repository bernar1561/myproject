from django.db import models
from django.conf import settings
from .manager import *


class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    status = models.IntegerField(verbose_name='статус', default=None, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(verbose_name='аватар', upload_to='users/%Y/%m/%d', default=None, blank=True)
    vk_link = models.URLField(verbose_name='ссылка на Vk', default=None, blank=True)
    fb_link = models.URLField(verbose_name='ссылка на facebook', default=None, blank=True)
    twitter_link = models.URLField(verbose_name='ссылка на twitter', default=None, blank=True)
    inst_link = models.URLField(verbose_name='ссылка на instagram', default=None, blank=True)
    objects = ProfileManager()
    # user_status = ProfileStatusManager()

    def __str__(self):
        return 'Профиль для пользователя {}'.format(self.user.username)


class Photo(models.Model):
    description = models.CharField(verbose_name='Описание', max_length=300, default=None, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    photo_like = models.IntegerField(verbose_name='Количество лайков', default=0, blank=True)

    def __str__(self):
        return 'Фотки пользователя %s %s' % (self.description, self.user.username)
