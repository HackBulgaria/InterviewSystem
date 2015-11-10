from django.core.management.base import BaseCommand
from course_interviews.helpers.generate_students import GenerateStudents
from interview_communicator.local_settings import f6s_address, f6s_application_name, f6s_api_key, f6s_page_count, f6s_page


class Command(BaseCommand):
    help = 'Generate students(applicants) with finalized forms by making a request to f6s'

    def handle(self, **options):

        students_generator = GenerateStudents(
            f6s_address, f6s_application_name, f6s_api_key, f6s_page_count, f6s_page)

        students_generator.generate_students()

        generated_students = students_generator.get_generated_students()
        finalized_students = students_generator.get_students_with_finalized_applications()
        students_in_base = students_generator.get_students_in_base()

        print(str(generated_students) + ' students were generated')
        print('There are ' + str(
            finalized_students) + ' students with finalized applications and ' + str(
            students_in_base) + ' in the base')
