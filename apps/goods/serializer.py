#序列化的目的：
#生成个列表，返回给前端,有两种方式：
    # 基于函数(function  base  view) (FBV)
    # 基于类 (class base view) (CBV)
from rest_framework import serializers
from goods.models import Goods,Banner,GoodsBanner
from goods.models import GoodsCategory

#序列化商品分类
class CategarySerializer3(serializers.ModelSerializer): # 三级分类
    class Meta:
        model= GoodsCategory
        fields = '__all__'

class CategarySerializer2(serializers.ModelSerializer): # 二级分类
    sub_cat = CategarySerializer3(many=True)
    class Meta:
        model= GoodsCategory
        fields = '__all__'

class CategarySerializer(serializers.ModelSerializer): # 一级分类
    sub_cat = CategarySerializer2(many=True)
    class Meta:
        model= GoodsCategory
        fields = '__all__'


# 序列化商品详情轮播图
class GoodsBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsBanner
        fields = ('image',) # ，必须加上

#序列化商品
class GoodsSerializer(serializers.ModelSerializer):
    category = CategarySerializer()  # 重写序列化
    images=GoodsBannerSerializer(many=True)  # 商品轮播图添加到序列化商品中
    class Meta:
        model = Goods
        fields = "__all__"

#序列化首页轮播图
class BannerSerializer(serializers.ModelSerializer):
    goods=GoodsSerializer()
    class Meta:
        model = Banner
        fields = "__all__"



