from course_interviews.models import Student, InterviewSlot
from datetime import datetime


class GenerateInterviews:

    def __init__(self):
        self.__students_without_interviews = 0
        self.__generated_interviews = 0

    def __inc_generated_interviews(self):
        self.__generated_interviews += 1

    def generate_interviews(self):
        students = list(Student.objects.all())
        slots = InterviewSlot.objects.all()
        today = datetime.now()
        for slot in slots:
            if slot.student or slot.buffer_slot or slot.teacher_time_slot.date < datetime.date(today):
                continue
            while len(students) != 0:
                student = students.pop(0)
                if not student.has_interview_date:
                    self.__inc_generated_interviews()
                    slot.student = student
                    student.has_interview_date = True
                    slot.save()
                    student.save()
                    break

    def get_students_without_interviews(self):
        count = 0
        all_students = Student.objects.all()

        for student in all_students:
            try:
                student.interviewslot
            except:
                count += 1
                pass

        return count

    def get_generated_interviews_count(self):
        return self.__generated_interviews
