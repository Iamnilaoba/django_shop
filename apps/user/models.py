from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    name = models.CharField("姓名", max_length=30, null=True, blank=True)
    birthday = models.DateField("出生年月", null=True, blank=True)
    gender = models.CharField("性别", max_length=6, choices=GENDER_CHOICES, default="female")
    mobile = models.CharField("电话", max_length=11, null=True, blank=True, help_text='手机号')

    class Meta:
        verbose_name = "用户信息" # 在admin中展示
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# post_save 模型保存的时候触发的信号
# settings.AUTH_USER_MODEL = 自定义的user,在settings配置文件中配置过
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

