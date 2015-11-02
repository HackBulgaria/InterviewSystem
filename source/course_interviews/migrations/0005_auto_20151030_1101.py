# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_interviews', '0004_auto_20151029_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='applied_course',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='skype',
            field=models.CharField(max_length=1100, default=None),
        ),
        migrations.AlterField(
            model_name='student',
            name='studies_at',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='works_at',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
    ]
