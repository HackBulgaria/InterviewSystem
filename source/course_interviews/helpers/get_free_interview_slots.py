from course_interviews.models import InterviewSlot
from datetime import datetime


def get_free_interview_slots():
    # Buffer slots are provided specially for the
    # students that can not attend their initial interview date

    # Buffer slots
    available_slots = InterviewSlot.objects.all().filter(
      buffer_slot=True, student__isnull=True).order_by('teacher_time_slot__date', 'start_time')

    # If no bufers are left, use other available empty slots after the current day
    if len(available_slots) == 0:
        today = datetime.now()
        available_slots = InterviewSlot.objects.all().filter(
            buffer_slot=False, student__isnull=True, teacher_time_slot__date__gt=datetime.date(
                today)).order_by('teacher_time_slot__date', 'start_time')

    return available_slots
