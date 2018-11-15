from django.urls import path,include,re_path
import xadmin
from django.views.static import serve
from django_shop.settings import MEDIA_ROOT
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from goods.views import GoodsView,CategaryView,BannerView

from rest_framework.routers import DefaultRouter
from user_operation.views import UserFavView
from trade.views import UserAddressView,ShoppingCartView,OrderInfoView,AlipayView

router=DefaultRouter()
# 商品收藏
router.register('user_fav',UserFavView)
# 商品列表
router.register(r'goods',GoodsView)
# 商品分类
router.register(r'category',CategaryView)
# 商品轮播图
router.register(r'banner',BannerView)
# 收货地址
router.register('useraddress',UserAddressView,basename='useraddress') # 必须加上basename
# 购物车
router.register('shoppingcart',ShoppingCartView,basename='shoppingcart')
# 订单详情
router.register('orderinfor',OrderInfoView,basename='orderinfor')


from django.shortcuts import render
def returnIndex(request):
    return render(request,'index.html')



urlpatterns = [
    re_path('^index/$',returnIndex), # 项目的首页
    re_path(r'^api-auth/', include('rest_framework.urls')),
    path('',include(router.urls)), # 各组件注册路由
    path('xadmin/', xadmin.site.urls), # 后台登录
    path('ueditor/',include('DjangoUeditor.urls' )),  # 加载富文本用
    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),  # 上传图片用
    path(r'api-token-auth/', views.obtain_auth_token),  # 通过用户名密码验证，生成token（自带验证）
    path('jwt-auth/', obtain_jwt_token),  # 通过用户名密码验证，生成token（JWT包验证）
    path('alipay/return/',AlipayView.as_view()), # 支付宝支付
    path('', include('social_django.urls', namespace='social')) # 第三方登录
]
