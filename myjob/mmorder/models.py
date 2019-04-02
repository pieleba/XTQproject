from django.contrib.auth.models import User
from django.db import models
from mmorder.views_constant import ORDER_STATUS_NOT_PAY


class FoodsType(models.Model):
    typename = models.CharField(max_length=20)
    note = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'mm_foodtype'


# class Category(models.Model):
#     name = models.CharField(max_length=50,
#                             verbose_name='分类名')
#     order_seq = models.IntegerField(verbose_name='排行')


class Foods(models.Model):
    fid = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=50)
    fcategory = models.CharField(max_length=20)
    fprice = models.FloatField()
    fpopnum = models.IntegerField()
    fimg = models.CharField(max_length=100)

    class Meta:
        db_table = 'mm_foods'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    state = models.IntegerField(default=ORDER_STATUS_NOT_PAY)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mm_order'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foods = models.ForeignKey(Foods, on_delete=models.CASCADE)
    cart_foods_num = models.IntegerField(default=1)
    is_selected = models.BooleanField(default=True)

    class Meta:
        db_table = 'mm_cart'


class Orderdetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    foods = models.ForeignKey(Foods, on_delete=models.CASCADE)
    order_foods_num = models.IntegerField()

    class Meta:
        db_table = 'mm_orderdetail'


class Knowledge(models.Model):
    title = models.CharField(max_length=60, verbose_name='小知识标题', primary_key=True)
    content = models.CharField(max_length=255, verbose_name='小知识内容')
    img = models.CharField(max_length=255, verbose_name='小知识图片')

    # search_date=models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'knowledge'
        verbose_name = '营养知识'
        verbose_name_plural = verbose_name
        ordering = ['title']
