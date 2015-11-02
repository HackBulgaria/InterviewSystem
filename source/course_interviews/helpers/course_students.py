from .get_students import AbstractGetStudents


class CourseStudents(AbstractGetStudents):

    def __init__(self, address, form_name, api_key, count, page, course):
        super().__init__(address, form_name, api_key, count, page)
        self.course = course
        self.__json = {
            "item": 0,
            "min": {
                "value": 0
            },
            "max": {
                "value": 0
            }
        }

    def generate_students_for_course(self):
        while (True):
            applications = self.get_student_applications()

            # Break loop if all students are added
            if applications["items_count"] == 0:
                break
            self.page += 1

            # If there is selected course and the application is
            # Finalized, inc() the students for the specified course
            for student in applications["data"]:
                if student["questions"][6]["field_response"] and \
                        student["questions"][6]["field_response"][0] == self.course:
                    self.__json["max"]["value"] += 1
                    if student["status"] == "Finalized":
                        self.__json["item"] += 1

    def get_json(self):
        return self.__json
