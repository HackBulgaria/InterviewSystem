from course_interviews.models import Student
from post_office import mail


class GenerateNewCoursesEmails:

    def __init__(self, template):
        self.template = template
        self.generated_emails = 0
        self.errors = 0

    def inc_errors(self):
        self.errors += 1

    def inc_generated_emails(self):
        self.generated_emails += 1

    def generate_new_courses_emails(self):
        # Emails are gona be send to all applicants that applied successfully
        recipients = [student for student in Student.objects.filter(
            has_received_new_courses_email=False)]

        for student in recipients:
            mail.send(
                recipients=[student.email],
                template=self.template,
                context={
                    'name': student.name,
                })
            try:
                self.inc_generated_emails()
                student.has_received_new_courses_email = True
                student.save()
            except Exception as e:
                self.inc_errors()
                student.has_received_new_courses_email = False
                student.save()
                print(e)
                pass

    def get_generated_emails(self):
        return self.generated_emails - self.errors

    def get_errors(self):
        return self.errors

    def get_students_with_generated_emails(self):
        return len(Student.objects.filter(has_received_new_courses_email=True))

    def get_students_without_generated_emails(self):
        return len(Student.objects.filter(has_received_new_courses_email=False))


class GenerateConfirmEmails(GenerateNewCoursesEmails):

    def __init__(self, template, confirm_interview_url, choose_interview_url):
        super().__init__(template)
        self.confirm_interview_url = confirm_interview_url
        self.choose_interview_url = choose_interview_url

    def generate_confirmation_emails(self):
        # Emails are gona be send to all applicants that have
        # interview date and didn't receive an email yet
        recipients = [student for student in Student.objects.filter(
            has_received_email=False,
            has_interview_date=True)]

        for student in recipients:
            mail.send(
                recipients=[student.email],
                template=self.template,
                context={
                    'name': student.name,
                    'applied_course': student.applied_course,
                    'skype': student.interviewslot.teacher_time_slot.teacher.skype,
                    'interview_date': student.interviewslot.teacher_time_slot.date,
                    'interview_start_time': student.interviewslot.start_time,
                    'confirm_interview_url': self.confirm_interview_url + student.uuid,
                    'choose_interview_url': self.choose_interview_url + student.uuid,
                })
            self.inc_generated_emails()
            student.has_received_email = True
            student.save()

    def get_generated_emails(self):
        return self.generated_emails - self.errors

    def get_errors(self):
        return self.errors

    def get_students_with_generated_emails(self):
        return len(Student.objects.filter(has_received_email=True))

    def get_students_without_generated_emails(self):
        return len(Student.objects.filter(has_received_email=False))
