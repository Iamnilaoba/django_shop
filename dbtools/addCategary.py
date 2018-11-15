#django 批量导入数据

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_shop.settings")

#django 1.6以下版本不需要写这个
import django
django.setup()

from dbtools.data.category_data import row_data  #拿取数据
from goods.models import GoodsCategory

def addCategory():
    for item in row_data:  # 一级分类
        g=GoodsCategory.objects.create(name=item['name'],code=item['code'],category_type=1)
        for item2 in item['sub_categorys']:  # 二级分类
            g1 = GoodsCategory.objects.create(name=item2['name'], code=item2['code'], category_type=2,
                                              parent_category=g)
            for item3 in item2['sub_categorys']:  # 三级分类
                GoodsCategory.objects.create(name=item3['name'], code=item3['code'], category_type=3,
                                             parent_category=g1)
addCategory()
