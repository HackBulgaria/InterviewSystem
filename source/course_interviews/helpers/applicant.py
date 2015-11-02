class Applicant:

    def __init__(
        self, name="", email="", skype="", phone_number="", applied_course="",
        first_task="", second_task="", third_task="", studies_at="", works_at=""
    ):
        self.name = name
        self.email = email
        self.skype = skype
        self.phone_number = phone_number
        self.applied_course = applied_course
        self.first_task = first_task
        self.second_task = second_task
        self.third_task = third_task
        self.studies_at = studies_at
        self.works_at = works_at

    def get_name(self):
        return self.name

    def get_email(self):
        # Example email returned from F6S:
        # "<a href=\"mailto:barcabg95&#64;abv.bg\" target=\"_blank\"
        # class=\"parsed-link\" rel=\"nofollow\">barcabg95&#64;abv.bg<\/a>"
        try:
            self.email = self.email.split(" ")[1][13:-1].replace("&#64;", "@")
        except:
            pass
        # F6S does not validate anything, so a wrong email comes as a string
        # Example:
        # "alexandermladjov@abv,bg"
        self.email = self.email.replace(",", ".")

        return self.email

    def get_skype(self):
        # If an email is passed instead of skype name (hot fix)
        if self.skype.startswith("<a href"):
            return self.skype.split(" ")[1][13:-1].replace("&#64;", "@")

        return self.skype

    def get_phone_number(self):
        # Remove any spaces or dashes used for the phone number
        self.phone_number = self.phone_number.replace(" ", "").replace("-", "")

        if self.phone_number.startswith('+359'):
            return self.phone_number
        else:
            self.phone_number = "+359" + self.phone_number[-9:]
            return self.phone_number

    def get_applied_course(self):
        return self.applied_course


# Example task returned from F6S:
# "<a href=\"https:\/\/github.com\/VladislavAtanasov\/HackBulgariaJavaCourseApplication\/blob\/
# master\/Task1\/Points.java\" target=\"_blank\" class=\"parsed-link\"rel=\"nofollow\">github.com\/
# VladislavAtanasov\/HackBulgariaJavaCourseApplication\/blob\/master\/Task1\/Points.java<\/a>"
    def get_first_task(self):
        task = ""
        try:
            task = self.first_task.split(" ")[1][6:-1]
        except:
            pass
        return task

    def get_second_task(self):
        task = ""
        try:
            task = self.second_task.split(" ")[1][6:-1]
        except:
            pass
        return task

    def get_third_task(self):
        task = ""
        try:
            task = self.third_task.split(" ")[1][6:-1]
        except:
            pass
        return task

    def get_studies_at(self):
        return self.studies_at

    def get_works_at(self):
        return self.works_at
