from course_interviews.models import InterviewerFreeTime, InterviewSlot
from datetime import datetime, timedelta


class GenerateInterviewSlots:

    def __init__(self, interview_time_length, break_time):
        self.interview_time_length = interview_time_length
        self.break_time = break_time
        self.__slots_generated = 0

    def __inc_slots_generated(self):
        self.__slots_generated += 1

    def __calculate_diff_in_time(self, start_time, end_time):
        start_delta = timedelta(
            hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second)
        end_delta = timedelta(
            hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second)
        return (end_delta - start_delta).seconds / 60

    def generate_interview_slots(self):
        teacher_time_slots = InterviewerFreeTime.objects.all().order_by('date')

        for slot in teacher_time_slots:
            # Check if slots are already generated for that time_slot
            # (by a previous invocation of manage.py generate_slots)
            if slot.has_generated_slots():
                continue

            # summarized free time of the interviewer
            free_time = self.__calculate_diff_in_time(slot.start_time, slot.end_time)
            # starting time of the first interview
            interview_start_time = slot.start_time

            while free_time >= self.interview_time_length:
                if slot.buffer_time:
                    interview_slot = InterviewSlot(
                        teacher_time_slot=slot,
                        start_time=interview_start_time,
                        buffer_slot=True)
                    interview_slot.save()
                else:
                    interview_slot = InterviewSlot(
                        teacher_time_slot=slot,
                        start_time=interview_start_time)
                    interview_slot.save()

                self.__inc_slots_generated()

                # Decrease the free time and change the starting time of the next interview
                free_time -= (self.interview_time_length + self.break_time)
                next_interview_date_and_time = datetime.combine(
                        slot.date, interview_start_time) + timedelta(
                        minutes=(self.interview_time_length + self.break_time))
                interview_start_time = next_interview_date_and_time.time()

    def get_generated_slots(self):
        return self.__slots_generated
