from course_interviews.models import InterviewSlot
from datetime import datetime


def get_free_interview_slots():
    # Buffer slots are provided specially for the
    # students that can not attend their initial interview date

    # Buffer days
    buffer_slots = InterviewSlot.objects.all().filter(
      buffer_slot=True).order_by('teacher_time_slot__date')

    available_slots = [slot for slot
                       in buffer_slots
                       if not slot.student]

    # If no bufers are left, use other available empty slots after the current day
    if len(available_slots) == 0:
        # The other slots are the ones that do not have students assigned to them
        other_slots = InterviewSlot.objects.all().order_by('teacher_time_slot__date', '-start_time')
        today = datetime.now()
        available_slots = [slot for slot
                           in other_slots
                           if not slot.student
                           and slot.teacher_time_slot.date > datetime.date(today)]

    return available_slots
