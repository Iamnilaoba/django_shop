from .models import UserAddress,ShoppingCart,OrderGoods,OrderInfo
from goods.models import Goods
from .serializer import UserAddressserializers,ShoppingCartserializers,\
    ShoppingCartDetailSerializers,OrderInfoSerializers,OrderInfoDetailSerializers
from rest_framework import viewsets,validators,mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# 收货地址
class UserAddressView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [BasicAuthentication,JSONWebTokenAuthentication]
    serializer_class = UserAddressserializers

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


# 购物车
class ShoppingCartView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [BasicAuthentication,JSONWebTokenAuthentication]
    lookup_field = 'goods_id'
    def get_serializer_class(self):
        if self.action=='list':
            return ShoppingCartDetailSerializers
        return ShoppingCartserializers

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):  # 添加购物车
        user = self.request.user
        goods_id = serializer.data['goods']
        # 提交购物车中商品
        shopCardGoods = ShoppingCart.objects.filter(user=user, goods_id=goods_id).first()
        # 仓库中商品
        gs = Goods.objects.filter(id=goods_id).first()
        if gs.goods_num >= serializer.data['nums']:
            gs.goods_num -= serializer.data['nums']  # 提交的购物车数量
            gs.save()  # 同步商品
            if shopCardGoods:  # 如果有这个商品
                shopCardGoods.nums += serializer.data['nums']
                shopCardGoods.save()  # 更新操作
            else:
                ShoppingCart.objects.create(goods_id=goods_id,
                                            nums=serializer.data['nums'],
                                            user=user)
        else:
            raise validators.ValidationError('商品不足')

        # 删除购物车中商品, 让商品的数量增加
    def perform_destroy(self, instance):
        # 通过购物车id 获取到一个购物车对象
        # 通过购物车对象获取到商品这个对象. 对象增加购物车中商品的数量
        # 这两个对象同步到数据库中
        shopcart = ShoppingCart.objects.get(pk=instance.pk)
        goods = instance.goods
        goods.goods_num += shopcart.nums
        shopcart.delete()  # 购物车对象删除
        goods.save()  # 商品进行保存

        # 更新 (获取到数量,修改数量)
        # put   127.0.0.1:8000/shop_cart/10/   {goods:'',nums:''}
    def perform_update(self, serializer):
        # 获取购物车
        shopCart = ShoppingCart.objects.get(pk=serializer.instance.pk)
        # 获取到这一次提交的商品对象
        goods = serializer.instance.goods
        # 差 = 购物中这个商品的数量-提交的数量
        c = shopCart.nums - serializer.initial_data['nums']
        # 更新购物车 (nums)
        shopCart.nums = serializer.initial_data['nums']  # 更新购物车中数量
        # 修改商品的数量
        goods.goods_num += c
        if goods.goods_num < 0:
            raise validators.ValidationError('商品不足')
        # 保存购物车
        shopCart.save()
        # 保存商品
        goods.save()

# 订单
class OrderInfoView(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin) :

    permission_classes = (IsAuthenticated,)  # 必须是自己
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]

    def get_serializer_class(self):
        if self.action=='retrieve':
            return OrderInfoDetailSerializers
        return OrderInfoSerializers

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer): # 新建订单
        # 保存订单信息, 清空购物车
        order = serializer.save() # 保存订单
        # 清空购物车 ,  在订单详情中保存购物车中数据
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts: # 循环购物车中没意见商品
            order_goods = OrderGoods() # 创建一个订单详情
            order_goods.goods = shop_cart.goods # 商品
            order_goods.goods_num = shop_cart.nums # 数量
            order_goods.order = order # 给订单赋值
            order_goods.save() # 保存订单详情
            # 清空购物车
            shop_cart.delete()
        return order


from trade.aliPay import AliPay
from datetime import datetime
from rest_framework.response import Response
from django.shortcuts import HttpResponseRedirect
from rest_framework.views import APIView


# 交易订单
class AlipayView(APIView):
    def get(self, request):
        processed_dict = {}
        #取出post里面的数据
        for key, value in request.GET.items():
            processed_dict[key] = value
        #把signpop掉，文档有说明
        sign = processed_dict.pop("sign", None)

        #生成一个Alipay对象
        alipay = AliPay(
            appid='2016092000553318',
            app_notify_url="http://39.105.77.148/alipay/return/",
            app_private_key_path='apps/trade/keys/proS.txt',  # 用户私钥
            alipay_public_key_path='apps/trade/keys/alipy.txt',  # 支付宝公钥
            debug=True,
            return_url="http://39.105.77.148/alipay/return/"
        )

        #进行验证
        verify_re = alipay.verify(processed_dict, sign)
        # 如果验签成功
        if verify_re is True:
            #商户网站唯一订单号
            order_sn = processed_dict.get('out_trade_no', None)
            #支付宝系统交易流水号
            trade_no = processed_dict.get('trade_no', None)
            #交易状态
            trade_status = processed_dict.get('trade_status', None)
            # 查询数据库中订单记录(根据订单号查询订单)
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 订单商品项
                order_goods = existed_order.goods.all() # 订单的详情
                # 商品销量增加订单中数值
                for order_good in order_goods:
                    goods = order_good.goods  # 获取到所有的商品
                    goods.sold_num += order_good.goods_num # 销量进行累加
                    goods.save() # 保存到数据库中

                # 更新订单状态
                existed_order.pay_status = trade_status # 修改订单的状态
                existed_order.trade_no = trade_no # 支付宝的流水号
                existed_order.pay_time = datetime.now() # 支付时间
                existed_order.save() # 更新订单信息
            #需要返回一个'success'给支付宝，如果不返回，支付宝会一直发送订单支付成功的消息
            return HttpResponseRedirect('http://39.105.77.148/index/')
        else:
            return Response('支付失败,sign不成功')


    def post(self, request):
        pass
        """
        处理支付宝的notify_url (必须是公网ip才行)
        """
        #存放post里面所有的数据
        processed_dict = {}
        #取出post里面的数据
        for key, value in request.POST.items():
            processed_dict[key] = value
        #把signpop掉，文档有说明
        sign = processed_dict.pop("sign", None)
        #生成一个Alipay对象
        alipay = AliPay(
            appid='2016092000553318',
            app_notify_url="http://39.105.77.148/alipay/return/",
            app_private_key_path='apps/trade/keys/proS.txt',  # 用户私钥
            alipay_public_key_path='apps/trade/keys/alipy.txt',  # 支付宝公钥
            debug=True,
            return_url="http://39.105.77.148/alipay/return/"
        )

        #进行验证
        verify_re = alipay.verify(processed_dict, sign)
        # 如果验签成功
        if verify_re is True:
            #商户网站唯一订单号
            order_sn = processed_dict.get('out_trade_no', None)
            #支付宝系统交易流水号
            trade_no = processed_dict.get('trade_no', None)
            #交易状态
            trade_status = processed_dict.get('trade_status', None)
            # 查询数据库中订单记录
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 订单商品项
                order_goods = existed_order.goods.all()
                # 商品销量增加订单中数值
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()
                # 更新订单状态
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            #需要返回一个'success'给支付宝，如果不返回，支付宝会一直发送订单支付成功的消息
            return Response("success")
