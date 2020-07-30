from django.urls import include, path
from .views import *

urlpatterns = [
    path("login", login, name="account"),
    # path("logout", logout, name="logout"),
    # path("getIdCaptcha",getCaptcha,name="getCaptch"),#获得验证码
    # path("verifStuId",verifStuId,name="verifStuId"),#绑定学号,学号验证
    path("myOrder",myorder,name="myOrder"),#我的订单
    path("myOrder2", myorder2, name="myOrder2"),  # 我的订单2
    path("myOrder3", myorder3, name="myOrder3"),  # 我的订单3
    path("myInfo",myInfo,name="myInfo"),
    path("myAddress",myAddress,name="myAddress"),#保存地址
    path("getAddress",getAddress,name="getAddress"), #获取地址
]