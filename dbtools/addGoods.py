#django 批量导入数据

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_shop.settings")

#django 1.6以下版本不需要写这个
import django
django.setup()

from goods.models import Goods
from dbtools.data.product_data import row_data  #拿取数据
from goods.models import GoodsCategory

def addGoods():
    for item in row_data:
        name=item['name']
        desc=item['desc']
        if not desc:
            desc=''
        sale_price=float(item['sale_price'].replace('￥','').replace('元',''))
        market_price = float(item['market_price'].replace('￥', '').replace('元', ''))  # '￥232元'
        goods_desc = item['goods_desc']
        images = item['images']
        goods_front_image=images[0]
        categorys = item['categorys']  # 分类的路径
        category = GoodsCategory.objects.filter(name=categorys[-1]).first()  # 分类
        Goods.objects.create(name=name,
                             goods_brief=desc,
                             shop_price=sale_price,
                             market_price=market_price,
                             goods_desc=goods_desc,
                             category=category,
                             goods_front_image=goods_front_image)
addGoods()
