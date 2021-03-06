# Generated by Django 2.0.6 on 2019-03-23 02:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_foods_num', models.IntegerField(default=1)),
                ('is_selectded', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'mm_cart',
            },
        ),
        migrations.CreateModel(
            name='Foods',
            fields=[
                ('fid', models.IntegerField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=50)),
                ('fcategory', models.CharField(max_length=20)),
                ('fprice', models.FloatField()),
                ('fpopnum', models.IntegerField()),
                ('fimg', models.CharField(max_length=100)),
                ('fstorenum', models.IntegerField()),
            ],
            options={
                'db_table': 'mm_foods',
            },
        ),
        migrations.CreateModel(
            name='FoodsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typename', models.CharField(max_length=20)),
                ('note', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'mm_foodtype',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('state', models.IntegerField(default=1)),
                ('time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mm_order',
            },
        ),
        migrations.CreateModel(
            name='Orderdetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_goods_num', models.IntegerField()),
                ('foods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mmorder.Foods')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mmorder.Order')),
            ],
            options={
                'db_table': 'mm_orderdetail',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='foods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mmorder.Foods'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
