from course_interviews.models import Student
from .get_students import AbstractGetStudents
from .applicant import Applicant


class GenerateStudents(AbstractGetStudents):

    def __init__(self, address, form_name, api_key, count, page):
        super().__init__(address, form_name, api_key, count, page)
        self.__students_with_finalized_applications = 0
        self.__errors = 0

    def __inc_errors(self):
        self.__errors += 1

    def __inc_students_with_finalized_applications(self):
        self.__students_with_finalized_applications += 1

    def __add_applicant(self, person):
        if person["status"] == "Finalized":
            applicant = Applicant(
                name=person["questions"][0]["question_response"],
                studies_at=person["questions"][1]["question_response"],
                works_at=person["questions"][2]["question_response"],
                first_task=person["questions"][3]["question_response"],
                second_task=person["questions"][4]["question_response"],
                third_task=person["questions"][5]["question_response"],
                applied_course=person["questions"][6]["field_response"][0],
                email=person["questions"][7]["question_response"],
                skype=person["questions"][8]["question_response"],
                phone_number=person["questions"][9]["question_response"],
            )
            student = Student(
                name=applicant.get_name(),
                studies_at=applicant.get_studies_at(),
                works_at=applicant.get_works_at(),
                first_task=applicant.get_first_task(),
                second_task=applicant.get_second_task(),
                third_task=applicant.get_third_task(),
                applied_course=applicant.get_applied_course(),
                email=applicant.get_email(),
                skype=applicant.get_skype(),
                phone_number=applicant.get_phone_number(),
            )
            try:
                self.__inc_students_with_finalized_applications()
                student.save()
            except Exception as e:
                self.__inc_errors()
                # the regular exception when saving student (that is already in the base) in the
                # base is email already taken - this error should be seen when
                # manage.py generate_students is invoked more than once
                # Error is not handled because of the different DB types
                print(e)
                pass

    def generate_students(self):
        while (True):
            applications = self.get_student_applications()

            # Break loop if all students are added
            if applications["items_count"] == 0:
                break

            self.page += 1
            for person in applications["data"]:
                self.__add_applicant(person)

    def get_errors(self):
        return self.__errors

    def get_generated_students(self):
        return self.__students_with_finalized_applications - self.__errors

    def get_students_with_finalized_applications(self):
        return self.__students_with_finalized_applications

    def get_students_in_base(self):
        return len(Student.objects.all())
