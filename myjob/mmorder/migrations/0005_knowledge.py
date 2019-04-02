# Generated by Django 2.0.6 on 2019-04-01 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmorder', '0004_auto_20190329_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Knowledge',
            fields=[
                ('title', models.CharField(max_length=60, primary_key=True, serialize=False, verbose_name='小知识标题')),
                ('content', models.CharField(max_length=255, verbose_name='小知识内容')),
                ('img', models.CharField(max_length=255, verbose_name='小知识图片')),
            ],
            options={
                'verbose_name': '营养知识',
                'verbose_name_plural': '营养知识',
                'db_table': 'knowledge',
                'ordering': ['title'],
            },
        ),
    ]
