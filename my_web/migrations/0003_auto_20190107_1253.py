# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_web', '0002_bbs_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='bbs',
            name='category',
            field=models.ForeignKey(default=1, to='my_web.Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bbs',
            name='author',
            field=models.ForeignKey(verbose_name='作者', to='my_web.BBS_user'),
        ),
        migrations.AlterField(
            model_name='bbs',
            name='create_at',
            field=models.DateTimeField(verbose_name='创建时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bbs',
            name='summary',
            field=models.CharField(verbose_name='概要', blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='bbs',
            name='title',
            field=models.CharField(verbose_name='标题', max_length=64),
        ),
        migrations.AlterField(
            model_name='bbs',
            name='update_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bbs',
            name='view_count',
            field=models.IntegerField(verbose_name='浏览数'),
        ),
    ]
