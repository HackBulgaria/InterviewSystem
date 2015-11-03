from django.core.management.base import BaseCommand
from course_interviews.helpers.generate_emails import GenerateConfirmEmails, GenerateNewCoursesEmails
from interview_communicator.local_settings import confirm_interview_url, choose_interview_url


class Command(BaseCommand):
    help = 'Generate emails for interview date confirmation'

    def handle(self, **options):
        # Generate emails for the new courses
        # template = 'new_courses'
        # email_generator = GenerateNewCoursesEmails(template)
        # email_generator.generate_new_courses_emails()

        template = 'interview_confirmation'

        email_generator = GenerateConfirmEmails(
            template, confirm_interview_url, choose_interview_url)

        email_generator.generate_confirmation_emails()

        generated_emails = email_generator.get_generated_emails()
        errors = email_generator.get_errors()
        students_with_emails = email_generator.get_students_with_generated_emails()
        students_without_emails = email_generator.get_students_without_generated_emails()

        print(str(
            generated_emails) + " confirmational emails were generated, " + str(
            errors) + " errors  occured")
        print("There are " + str(
            students_with_emails) + " students with generated confirmational emails")
        print(str(students_without_emails) + " students still do NOT have confirmational emails")
