from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import viewsets,mixins
from goods.models import Goods,GoodsCategory,Banner,GoodsBanner
from goods.serializer import GoodsSerializer,CategarySerializer,BannerSerializer,GoodsBannerSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework import filters as drffilters

# 1.用Django里的视图View
# class GoodsView(View):
#     def get(self,request):
#         gs=Goods.objects.all()
#         lst=GoodsSerializer(gs,many=True)
#         return JsonResponse(lst.data,safe=False)

# 2.用rest_framework里的View
# class GoodsView(APIView):
#     def get(self, request):
#         gs = Goods.objects.all()
#         lst = GoodsSerializer(gs,many=True)
#         return Response(lst.data)

#ListCreateAPIView
import django_filters
from django_filters import rest_framework as filters
#自定义过滤器  # 可自定义查询范围
class ProductFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(field_name="market_price", lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name="market_price", lookup_expr='lte')
    name = filters.CharFilter(field_name='name',lookup_expr='contains')
    top_category = filters.NumberFilter(field_name='category',method='filterGoodsByCategary')

    def filterGoodsByCategary(self,queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))
    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax','name','top_category']

#重写分页
class GoodPagePageNumberPagination(PageNumberPagination):
    page_query_param = 'page' # 分页提交的参数
    page_size = 12
    max_page_size = 100

#商品给前端
class GoodsView(viewsets.ReadOnlyModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    # 功能
    pagination_class = GoodPagePageNumberPagination  # 定义局部的分页
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,drffilters.OrderingFilter,drffilters.SearchFilter)  # 局部注册过滤的控件
    filterset_class = ProductFilter  # 用自定义的类过滤器查询
    ordering_fields=('sold_num','shop_price')  # 排序
    search_param=('name',) # 根据名字查询
    from rest_framework.permissions import AllowAny,IsAuthenticated  # 认证用户访问状态
    #permission_classes = (AllowAny,)  #任何人
    permission_classes = (IsAuthenticated,)  #需登录

#商品分类给前端
class CategaryView(viewsets.ReadOnlyModelViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1).all()
    serializer_class = CategarySerializer

#首页轮播图给前端
class BannerView(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Banner.objects.all().order_by('index')[0:4]
    serializer_class = BannerSerializer

