import requests


class AbstractGetStudents:

    def __init__(self, address, form_name, api_key, count, page):
        self.address = address
        self.form_name = form_name
        self.api_key = api_key
        self.count = count
        self.page = page

    def get_student_applications(self):
        url = self.address + self.form_name + "/applications?api_key=" \
            + self.api_key + "&page=" + str(self.page) + "&count=" + str(self.count)
        applications = requests.get(url).json()
        return applications
