from django.db import models

from goods.models import Goods
from rest_framework.authentication import get_user_model
User=get_user_model()
from datetime import datetime

# 用户收藏表
class UserFav(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    goods=models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name='商品',help_text='商品id')
    add_time=models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name='用户收藏'
        verbose_name_plural=verbose_name
        unique_together=('user','goods') # 定义联合唯一

    def __str__(self):
        return self.user.username
