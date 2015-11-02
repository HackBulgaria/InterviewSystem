# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_interviews', '0005_auto_20151030_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='has_received_new_courses_email',
            field=models.BooleanField(default=False),
        ),
    ]
