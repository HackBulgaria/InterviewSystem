# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_interviews', '0006_student_has_received_new_courses_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewerfreetime',
            name='buffer_time',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='interviewslot',
            name='buffer_slot',
            field=models.BooleanField(default=False),
        ),
    ]
