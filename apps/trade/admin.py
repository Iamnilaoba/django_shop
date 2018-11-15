from django.contrib import admin

import xadmin
from .models import UserAddress,ShoppingCart,OrderInfo,OrderGoods

class UserAddressxadmin(object):
    pass

class ShoppingCartxadmin(object):
    pass

class OrderInfoxadmin(object):
    pass

class OrderGoodsxadmin(object):
    pass

xadmin.site.register(UserAddress,UserAddressxadmin)
xadmin.site.register(ShoppingCart,ShoppingCartxadmin)
xadmin.site.register(OrderInfo,OrderInfoxadmin)
xadmin.site.register(OrderGoods,OrderGoodsxadmin)
