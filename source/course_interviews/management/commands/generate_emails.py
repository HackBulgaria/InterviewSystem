from django.core.management.base import BaseCommand
from course_interviews.helpers.generate_confirm_emails import GenerateConfirmEmails


class Command(BaseCommand):
    help = 'Generate emails for interview date confirmation'

    def handle(self, **options):
        template = 'interview_confirmation'
        confirm_interview_url = "http://localhost:8000/confirm-interview/"
        choose_interview_url = "http://localhost:8000/choose-interview/"

        confirm_email_generator = GenerateConfirmEmails(
            template, confirm_interview_url, choose_interview_url)

        confirm_email_generator.generate_emails()

        generated_emails = confirm_email_generator.get_generated_emails()
        errors = confirm_email_generator.get_errors()
        students_with_emails = confirm_email_generator.get_students_with_generated_email()
        students_without_emails = confirm_email_generator.get_students_without_generated_email()

        print(str(
            generated_emails) + " confirmational emails were generated, " + str(
            errors) + " errors  occured")
        print("There are " + str(
            students_with_emails) + " students with generated confirmational emails")
        print(str(students_without_emails) + " students still do NOT have confirmational emails")
