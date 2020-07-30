from django.db import models
from account.models import user
from django.utils import timezone

# Create your models here.
#跑腿订单

class order2(models.Model):
    value_low = 0
    value_middle = 1
    value_high = 2

    # value_choices = (
    #     (value_low, "low value"),
    #     (value_middle, "normal value"),
    #     (value_high, "high value"),
    # )

    jiangan=1
    wangjiang=2
    huaxi=3
    uncompleted = 0
    completing = 1
    uncommented = 2
    completed = 3
    canceled = 4
    expired = 5
    order_campus_choices=(
        (jiangan, "jiangan"),  # 未完成
        (wangjiang, "wangjiang"),  # 未完成
        (huaxi, "huaxi"),  # 未完成
    )
    order_status_choices = (
        (uncompleted, "uncompleted"),  # 未完成
        (completing, "completing"),  # 进行中
        (uncommented, "uncommented"),  # 未评价
        (completed, "completed"),  # 已完成
        (canceled, "canceled"),  # 已取消
        (expired, "expired"),  # 已过期
    )

    orderid = models.AutoField(max_length=30, unique=True, primary_key=True)
    # value = models.IntegerField(verbose_name="价值", choices=value_choices, default=value_high)
    createTime = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    expireDateTime = models.DateTimeField(verbose_name="过期时间")
    order_owner = models.ForeignKey(user, verbose_name="订单主人", null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name="owner_orders2")
    # 接订单的人
    free_lancer = models.ForeignKey(user, verbose_name="接单人", null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name="lancer_orders2")
    # 酬劳
    money = models.DecimalField(max_digits=50, decimal_places=4, default=0, verbose_name="酬劳")
    goods_weight = models.DecimalField(max_digits=50, decimal_places=4, default=0, verbose_name="物品重量")
    # # 地点
    pos = models.CharField(verbose_name="地点", max_length=256, default="快递街")
    # 校区
    campus = models.CharField(verbose_name="校区", max_length=256)
    #kuaidi = models.CharField(verbose_name="快递商", max_length=256)
    goods_introduction = models.CharField(verbose_name="商品简介", blank=True, null=True, max_length=256)
    goods_category = models.CharField(verbose_name="商品种类", blank=True, null=True, max_length=256)
    received_pos = models.CharField(verbose_name="收货地址", max_length=256)
    order_status = models.IntegerField(verbose_name="订单状态", choices=order_status_choices, default=uncompleted)
    goods_img = models.CharField(verbose_name="图片url", max_length=2000, default="/static/account/img/bob.jpg")
    kind = models.CharField(verbose_name="跑腿类型", blank=True, null=True, max_length=256)

    # #hidden information
    # phone_number = models.CharField(verbose_name="电话号码",max_length=11.)
    # #取件码
    # code = models.CharField(verbose_name="取件码",max_length=64)
    # #收货人姓名
    # owner_name = models.CharField(verbose_name="主人名",max_length=256)
    hidden_info = models.TextField(verbose_name="隐藏的信息", null=True, blank=True)


# 包含收件手机号 取件码 以及一切相关的信息

class Meta:
    verbose_name = "订单"
    verbose_name_plural = "订单s"


def __str__(self):
    return self.orderid + " " + order2.value_choices[self.value][1]
