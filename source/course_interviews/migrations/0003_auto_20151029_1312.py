# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_interviews', '0002_auto_20151028_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='teacher',
            name='last_name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
