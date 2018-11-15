from django.contrib import admin
import xadmin
from goods.models import Goods,Banner,GoodsBanner
# Register your models here.
class GoodsAdmin(object):
    # 显示的列
    list_display = ["name", "click_num", "sold_num", "fav_num", "goods_num"]

    # 允许这个字段富文本编辑器展示
    style_fields = {"goods_desc": "ueditor"}

class BannerAdmin(object):
    list_display=['image','index']


class GoodsBannerAdmin(object):
    list_display=['image','index']


xadmin.site.register(Goods,GoodsAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(GoodsBanner,GoodsBannerAdmin)
