from django.db import models
from account.models import user

# Create your models here.

class credit(models.Model):
    ctraderecord = models.IntegerField(verbose_name="交易记录")
    cpoint = models.IntegerField(verbose_name="信用积分", default=100)
    cordernum = models.IntegerField(verbose_name="接单数量")
    csendnum = models.IntegerField(verbose_name="发单数量")
    cscore_detail = models.IntegerField(verbose_name="积分明细")
    csno = models.ForeignKey(user, verbose_name="用户", on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="credit_user")

