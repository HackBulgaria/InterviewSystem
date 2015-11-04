# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_interviews', '0007_auto_20151103_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewslot',
            name='student',
            field=models.OneToOneField(to='course_interviews.Student', blank=True, null=True),
        ),
    ]
