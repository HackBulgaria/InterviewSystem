# -*- coding: utf-8 -*-
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_extensions.db.fields import UUIDField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid


class SiteUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email address must be set')

        email = SiteUserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class Teacher(AbstractBaseUser, PermissionsMixin):

    objects = SiteUserManager()

    email = models.EmailField(unique=True, blank=False)
    skype = models.CharField(
        default=None,
        max_length=50,
        help_text='Enter the skype of the teacher!')
    first_name = models.CharField(default="", max_length=50)
    last_name = models.CharField(default="", max_length=50)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'skype']

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name()


class Student(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    skype = models.CharField(default=None, max_length=1100)
    phone_number = PhoneNumberField(blank=True)
    applied_course = models.CharField(null=True, blank=True, max_length=1100)
    first_task = models.URLField(null=True, blank=True)
    second_task = models.URLField(null=True, blank=True)
    third_task = models.URLField(null=True, blank=True)
    studies_at = models.CharField(blank=True, null=True, max_length=1100)
    works_at = models.CharField(null=True, blank=True, max_length=1100)

    # possible_rating is number between 1 and 10 to be selected in the integer field
    possible_ratings = [(i, i) for i in range(11)]
    code_skills_rating = models.IntegerField(
        default=0,
        choices=possible_ratings,
        help_text='Оценка върху уменията на кандидата да пише'
        ' код и знанията му върху базови алгоритми')
    code_design_rating = models.IntegerField(
        default=0,
        choices=possible_ratings,
        help_text='Оценка върху уменията на кандидата да "съставя'
        ' програми" и да разбива нещата по парчета + базово OOP')
    fit_attitude_rating = models.IntegerField(
        default=0,
        choices=possible_ratings,
        help_text='Оценка на интервюиращия в зависимост от'
        ' усета му за човека (става ли за курса)')
    teacher_comment = models.TextField(
        null=True,
        blank=True,
        help_text='Коментар на интервюиращия за цялостното представяне на кандидата')
    has_interview_date = models.BooleanField(default=False)
    has_received_email = models.BooleanField(default=False)
    has_confirmed_interview = models.BooleanField(default=False)
    has_been_interviewed = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    uuid = UUIDField(version=4, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.name


class InterviewerFreeTime(models.Model):
    teacher = models.ForeignKey(Teacher)
    date = models.DateField(blank=False, null=True)
    start_time = models.TimeField(blank=False, null=True)
    end_time = models.TimeField(blank=False, null=True)

    # method for checking if the slots for the specific interviewer free time
    # are already generated. Method is called by /helpers/generate_interview_slots.py
    def has_generated_slots(self):
        return self.interviewslot_set.exists()

    def __str__(self):
        return str(self.date) + " - from " + str(self.start_time) + " to " + str(self.end_time)


class InterviewSlot(models.Model):
    teacher_time_slot = models.ForeignKey(InterviewerFreeTime)
    student = models.OneToOneField(Student, null=True)
    start_time = models.TimeField(blank=False, null=True)
