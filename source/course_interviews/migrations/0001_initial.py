# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import phonenumber_field.modelfields
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('skype', models.CharField(help_text='Enter the skype of the teacher!', default=None, max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterviewerFreeTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField(null=True)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InterviewSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('start_time', models.TimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('skype', models.CharField(default=None, max_length=110)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128)),
                ('applied_course', models.CharField(blank=True, max_length=110, null=True)),
                ('first_task', models.URLField(blank=True, null=True)),
                ('second_task', models.URLField(blank=True, null=True)),
                ('third_task', models.URLField(blank=True, null=True)),
                ('studies_at', models.CharField(blank=True, max_length=110, null=True)),
                ('works_at', models.CharField(blank=True, max_length=110, null=True)),
                ('code_skills_rating', models.IntegerField(help_text='Оценка върху уменията на кандидата да пише код и знанията му върху базови алгоритми', default=0, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('code_design_rating', models.IntegerField(help_text='Оценка върху уменията на кандидата да "съставя програми" и да разбива нещата по парчета + базово OOP', default=0, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('fit_attitude_rating', models.IntegerField(help_text='Оценка на интервюиращия в зависимост от усета му за човека (става ли за курса)', default=0, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('teacher_comment', models.TextField(help_text='Коментар на интервюиращия за цялостното представяне на кандидата', blank=True, null=True)),
                ('has_interview_date', models.BooleanField(default=False)),
                ('has_received_email', models.BooleanField(default=False)),
                ('has_confirmed_interview', models.BooleanField(default=False)),
                ('has_been_interviewed', models.BooleanField(default=False)),
                ('is_accepted', models.BooleanField(default=False)),
                ('uuid', django_extensions.db.fields.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='interviewslot',
            name='student',
            field=models.OneToOneField(to='course_interviews.Student', null=True),
        ),
        migrations.AddField(
            model_name='interviewslot',
            name='teacher_time_slot',
            field=models.ForeignKey(to='course_interviews.InterviewerFreeTime'),
        ),
    ]
