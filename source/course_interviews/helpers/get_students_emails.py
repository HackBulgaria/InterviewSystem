from .get_students import AbstractGetStudents


# This class is helper for the api/get-emails view
class GetStudentsEmails(AbstractGetStudents):

    def __init__(self, address, form_name, api_key, count, page, courses):
        super().__init__(address, form_name, api_key, count, page)
        self.courses = courses
        self.__json = {
            "No course selected": [],
        }
        self.__generate_courses_for_json()

    def __generate_courses_for_json(self):
        for course in self.courses:
            self.__json[course] = []

    def __get_validated_email(self, email):
        try:
            # F6S Where is your validation?!?
            email = email.split(" ")[1][13:-1].replace("&#64;", "@").replace(",", ".")
        except:
            pass
        email = email.replace(",", ".")
        return email

    def generate_students_emails(self):
        while (True):
            applications = self.get_student_applications()

            # Break loop if all students are added
            if applications["items_count"] == 0:
                break
            self.page += 1

            for student in applications["data"]:
                email = self.__get_validated_email(student["questions"][7]["question_response"])
                # Check if application is still in progress and there is email
                if student["status"] == "In Progress" and email != "":
                    # Check if there is selected course
                    if student["questions"][6]["field_response"]:
                        course = student["questions"][6]["field_response"][0]
                        self.__json[course].append(email)
                    else:
                        self.__json["No course selected"].append(email)

    def get_json(self):
        return self.__json
