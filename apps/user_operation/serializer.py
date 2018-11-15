from .models import UserFav
from rest_framework import serializers
from apps.goods.serializer import GoodsSerializer
from rest_framework.validators import UniqueTogetherValidator  # 校验是不是唯一的

#序列化商品收藏
class UserFavserializers(serializers.ModelSerializer):
    # CurrentUserDefault()：这个小括号必须加上否则回报缺少serializers.fields这个错误
    user=serializers.HiddenField(default=serializers.CurrentUserDefault()) #拿到用户的信息隐藏起来不给前台
    class Meta:
        model=UserFav
        validators=[
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user','goods'),
                message='已经收藏'
            )
        ]
        fields='__all__'

class UserFavDetailSerializers(serializers.ModelSerializer):
    goods=GoodsSerializer()
    class Meta:
        model=UserFav
        fields=('id','goods')

