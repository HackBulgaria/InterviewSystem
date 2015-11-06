from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import generics
from .serializers import InterviewSlotSerializer
from .models import Student, InterviewSlot
from .helpers.course_students import CourseStudents
from .helpers.get_students_emails import GetStudentsEmails, GetAllStudentsEmails
from .helpers.get_free_interview_slots import get_free_interview_slots
from interview_communicator.local_settings import (f6s_address, f6s_application_name, f6s_api_key,
                                                   f6s_page_count, f6s_page)


# Function providing the students that applied for a specific course and submited their applications
def get_students(request, course):
    if course == "Csharp":
        course = "Programming 101 with C#"
    elif course == "Java":
        course = "Programming 101 with Java"
    elif course == "Ruby":
        course = "Programming 101 with Ruby"
    elif course == "Python":
        course = "Programming 101 with Python"

    course_students_generator = CourseStudents(
        f6s_address, f6s_application_name, f6s_api_key, f6s_page_count, f6s_page, course)

    course_students_generator.generate_students_for_course()
    json = course_students_generator.get_json()

    return JsonResponse(json)


# Function for the emails of all applicants that left email in their F6S application,
# but did not yet submit their tasks - we are gona send them a reminder email for submition
@staff_member_required
def get_emails(request):
    courses = [
        "Programming 101 with C#",
        "Programming 101 with Java",
        "Programming 101 with Ruby",
        "Programming 101 with Python"
    ]

    get_students_emails_generator = GetStudentsEmails(
        f6s_address, f6s_application_name, f6s_api_key, f6s_page_count, f6s_page, courses)

    get_students_emails_generator.generate_students_emails()
    json = get_students_emails_generator.get_json()

    return JsonResponse(json)


# Function for all of the emails given in the F6S form
@staff_member_required
def get_all_emails(request):
    courses = []  # Get all courses

    get_students_emails_generator = GetAllStudentsEmails(
        f6s_address, f6s_application_name, f6s_api_key, f6s_page_count, f6s_page, courses)

    get_students_emails_generator.generate_students_emails()
    json = get_students_emails_generator.get_json()

    return JsonResponse((", ").join(json["students"]), safe=False)


# Function serving interview slots to HandleBars
# TODO: use DRF
def get_interview_slots(request):
    json = []
    available_slots = get_free_interview_slots()

    for slot in available_slots:
        json.append({
            "date": slot.teacher_time_slot.date,
            "time": slot.start_time,
            "slot_id": slot.id
            })

    return JsonResponse(json, safe=False)


class GetInterviewSlots(generics.ListCreateAPIView):
    queryset = get_free_interview_slots()
    serializer_class = InterviewSlotSerializer


def confirm_student_interview(request):
    if request.POST:
        token = request.POST["token"]
        student = get_object_or_404(Student, uuid=token)

        if not student.has_interview_date:
            raise HttpResponseNotFound(
                "Student does not have an interview date")

        student.has_confirmed_interview = True
        student.save()
        return HttpResponse("OK")


def confirm_slot(request):
    if request.POST:
        slot_id = request.POST["slot_id"]
        student_uuid = request.POST["student_uuid"]

        slot = get_object_or_404(InterviewSlot, id=slot_id)
        student = get_object_or_404(Student, uuid=student_uuid)

        if slot.student:
            return HttpResponseNotFound(
                "This interview slot is already taken! Please select another one")

        if student.has_confirmed_interview:
            return HttpResponseNotFound(
                "You already confirmed your interview. You can't choose another one.")

        # The auto generated slot student already has should become free
        try:
            vacate_slot = InterviewSlot.objects.get(student=student)
            vacate_slot.student = None
            vacate_slot.save()
        except:
            pass

        slot.student = student
        student.has_interview_date = True
        student.has_confirmed_interview = True

        slot.save()
        student.save()

        return HttpResponse("OK")
