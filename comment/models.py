from django.db import models
from order.models import order


# Create your models here.

class comment(models.Model):
    id = models.AutoField(primary_key=True)
    owner_star = models.IntegerField(verbose_name="评分", null=True, blank=True, default=5)
    owner_text = models.TextField("评价内容", null=True, blank=True, default="")
    order = models.OneToOneField(verbose_name="发单人订单", to=order, on_delete=models.CASCADE, null=True, blank=True,
                                 default=None)
    lancer_star = models.IntegerField(verbose_name="接单人评分", null=True, blank=True, default=5)
    lancer_text = models.TextField(verbose_name="评价内容", null=True, blank=True, default="")
    owner_commented = models.BooleanField(verbose_name="发单人是否评价", default=False)
    lancer_commented = models.BooleanField(verbose_name="接单人是否评价", default=False)

    class Meta:
        verbose_name = "评价"
        verbose_name_plural = "评价s"
