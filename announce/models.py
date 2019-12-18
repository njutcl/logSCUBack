from django.db import models


# Create your models here.
class announcement(models.Model):
    id = models.AutoField(max_length=30, unique=True, primary_key=True)
    title = models.TextField(verbose_name="标题",default="", max_length=20)
    content = models.TextField(verbose_name="内容",default="", max_length=200)
    createdTime = models.DateTimeField(verbose_name="创建时间", auto_now=True)

    # models.IntegerField(verbose_name="公告种类", choices=order_status_choices, default=uncompleted)
    def __str__(self):
        return self.content[:]

    class Meta:
        verbose_name = "公告"
        verbose_name_plural = "公告"
