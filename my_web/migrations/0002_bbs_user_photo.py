# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bbs_user',
            name='photo',
            field=models.ImageField(default='upload_imgs/user-1.jpg', upload_to='upload_imgs/'),
        ),
    ]
