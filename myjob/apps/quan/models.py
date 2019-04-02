from django.db import models

# Create your models here.


class QuanActive(models.Model):

    publish_date = models.DateField(verbose_name='发布时间',
                                    auto_now_add=True)

    valid_days = models.IntegerField(verbose_name='有效天数',
                                     default=30)

    vulumns = models.IntegerField(verbose_name='限发量',
                                  default=10000)

    title = models.CharField(verbose_name='活动名称',
                             max_length=200)

    note = models.TextField(verbose_name='备注',
                            null=True,
                            blank=True)

    class Meta:
        db_table = 't_quan_active'
        verbose_name = '优惠券活动'
        verbose_name_plural = verbose_name
        ordering = ['-publish_date']
