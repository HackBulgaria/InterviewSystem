from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Student
from .apis import *


def index(request):
    return render(request, "index.html", locals())


def confirm_interview(request, token):
    student = get_object_or_404(Student, uuid=token)
    teacher = student.interviewslot.teacher_time_slot.teacher

    return render(request, "confirm_interview.html", locals())


def choose_interview(request, token):
    student = get_object_or_404(Student, uuid=token)

    if student.has_confirmed_interview:
        raise Http404("Student already has an interview date")

    return render(request, "choose_interview.html", locals())
