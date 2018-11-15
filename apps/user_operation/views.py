from .serializer import UserFavserializers,UserFavDetailSerializers
from .models import UserFav
from rest_framework import mixins,viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import BasicAuthentication,SessionAuthentication

# 商品收藏
class UserFavView(viewsets.ModelViewSet):
    queryset = UserFav.objects.all()

    def get_serializer_class(self):  # 多类序列化（等价于serializer_class = A和B）
        if self.action == 'list':   # action两种 list和retrieve
            return UserFavDetailSerializers
        return UserFavserializers

    def get_queryset(self):  # 拿到用户信息
        return UserFav.objects.filter(user=self.request.user)

    permission_classes = (IsAuthenticated,)  # 权限
    authentication_classes = [BasicAuthentication,JSONWebTokenAuthentication]

    lookup_field = 'goods_id' # 查找



