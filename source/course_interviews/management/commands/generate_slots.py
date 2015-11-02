from django.core.management.base import BaseCommand
from course_interviews.helpers.generate_interview_slots import GenerateInterviewSlots


class Command(BaseCommand):
    help = 'Generate interview slots using the free time of the teachers(interviewers)'

    def handle(self, **options):
        interview_length = 20
        break_between_interviews = 10

        interview_slots_generator = GenerateInterviewSlots(
            interview_length, break_between_interviews)

        interview_slots_generator.generate_interview_slots()
        generated_slots = interview_slots_generator.get_generated_slots()

        print(str(generated_slots) + ' slots were generated')
