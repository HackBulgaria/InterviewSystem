# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_interviews', '0003_auto_20151029_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(max_length=50, default=''),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='last_name',
            field=models.CharField(max_length=50, default=''),
        ),
    ]
