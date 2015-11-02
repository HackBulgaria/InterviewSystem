from django.core.management.base import BaseCommand
from course_interviews.helpers.generate_interviews import GenerateInterviews


class Command(BaseCommand):
    help = 'Generate interviews using the free slots and the students without interviews'

    def handle(self, **options):
        interview_generator = GenerateInterviews()
        interview_generator.generate_interviews()

        students_without_interviews = interview_generator.get_students_without_interviews()
        generated_interviews = interview_generator.get_generated_interviews_count()

        print(str(generated_interviews) + ' interviews were generated')
        print(str(students_without_interviews) + ' students do not have interview date')
