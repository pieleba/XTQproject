# Generated by Django 2.0.6 on 2019-03-29 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmorder', '0003_auto_20190328_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='order_goods_num',
            new_name='order_foods_num',
        ),
    ]