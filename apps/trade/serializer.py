from .models import UserAddress,ShoppingCart,OrderGoods,OrderInfo
from goods.models import Goods
from goods.serializer import GoodsSerializer
from rest_framework import serializers

# 收货地址序列化
class UserAddressserializers(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=UserAddress
        fields='__all__'

# 购物车序列化
class ShoppingCartserializers(serializers.Serializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums=serializers.IntegerField(required=True,min_value=1,
                                  error_messages={
                                      'required':'nums必须写',
                                      'min_value':'最小为1'
                                  })
    goods=serializers.PrimaryKeyRelatedField(many=False,queryset=Goods.objects.all())
    class Meta:
        model=ShoppingCart
        fields='__all__'
# 列表
class ShoppingCartDetailSerializers(serializers.ModelSerializer): #只希望序列化goods_id，不希望序列化其他字段
    goods=GoodsSerializer()
    class Meta:
        model=ShoppingCart
        fields='__all__'

# 订单详情序列化
class OrderGoodsSerializers(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = '__all__'


# 订单简要信息
class OrderInfoSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # 订单号唯一
    order_sn = serializers.CharField(read_only=True)
    # 微信支付会用到
    nonce_str = serializers.CharField(read_only=True)
    # 支付宝交易号
    trade_no = serializers.CharField(read_only=True)
    # 支付状态
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    # 支付的url
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self,obj):
        from trade.aliPay import AliPay
        alipay=AliPay(
            appid='2016092000553318',
            app_notify_url="http://39.105.77.148/alipay/return/",
            app_private_key_path='apps/trade/keys/proS.txt', # 用户私钥
            alipay_public_key_path='apps/trade/keys/alipy.txt', # 支付宝公钥
            debug=True,
            return_url="http://39.105.77.148/alipay/return/"
        )

        url = alipay.direct_pay(
            # 订单标题
            subject=obj.order_sn,
            # 我们商户自行生成的订单号
            out_trade_no=obj.order_sn,
            # 订单金额
            total_amount=obj.order_mount,
            # 成功付款后跳转到的页面，return_url同步的url
            return_url="http://39.105.77.148/alipay/return/"
        )
        # 将生成的请求字符串拿到我们的url中进行拼接
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url


    class Meta:
        model = OrderInfo
        fields = '__all__'

    def generate_order_sn(self):
        # 生成订单号
        # 当前时间+userid+随机数
        from random import Random
        import time
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    # 订单号  订单时间用户id随机数
    def create(self, validated_data):
        validated_data['order_sn'] = self.generate_order_sn() # 必须是唯一
        return OrderInfo.objects.create(**validated_data)


class OrderInfoDetailSerializers(serializers.ModelSerializer):
    goods = OrderGoodsSerializers(many=True)
    class Meta:
        model = OrderInfo
        fields = '__all__'



