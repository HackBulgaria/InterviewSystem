from course_interviews.models import Student, Teacher, InterviewerFreeTime, InterviewSlot

from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase


class ViewsTests(TestCase):

    def setUp(self):
        self.teacher_admin = Teacher.objects.create_superuser(
            "admin@admin.com", "123", skype="admin_hackbulgaria")

        self.teacher_user1 = Teacher.objects.create_user(
            "user1@user.com", "123", skype="user1_user")

        self.teacher_user2 = Teacher.objects.create_user(
            "user2@user.com", "123", skype="user2_user")

        teacher_user_permission_names = [
            'add_interviewerfreetime',
            'change_interviewerfreetime',
            'delete_interviewerfreetime',
            'change_interviewslot',
            'add_student',
            'change_student',
        ]

        teacher_user_permissions = Permission.objects.filter(
            codename__in=teacher_user_permission_names
        )

        self.teacher_group = Group.objects.create(name='Editor')
        self.teacher_group.permissions = teacher_user_permissions
        self.teacher_group.save()

        self.teacher_user1.first_name = "Ivo"
        self.teacher_user1.last_name = "Radov"
        self.teacher_user1.is_staff = True
        self.teacher_user1.groups.add(self.teacher_group)
        self.teacher_user1.save()

        self.teacher_user2.first_name = "Rado"
        self.teacher_user2.last_name = "Ivov"
        self.teacher_user2.is_staff = True
        self.teacher_user2.groups.add(self.teacher_group)
        self.teacher_user2.save()

        self.teacher_free_time1 = InterviewerFreeTime.objects.create(
            teacher=self.teacher_user1,
            date="2016-10-30",
            start_time="15:00",
            end_time="16:00")

        self.teacher_free_time2 = InterviewerFreeTime.objects.create(
            teacher=self.teacher_user2,
            date="2016-10-31",
            start_time="16:00",
            end_time="17:00")

        self.interview_slot1 = InterviewSlot.objects.create(
            teacher_time_slot=self.teacher_free_time1,
            start_time="15:00")

        self.interview_slot2 = InterviewSlot.objects.create(
            teacher_time_slot=self.teacher_free_time2,
            start_time="16:00")

        self.student1 = Student.objects.create(
            name="Student One",
            email="student1@student.com",
            skype="student_one_skype")

        self.student2 = Student.objects.create(
            name="Student Two",
            email="student2@student.com",
            skype="student_two_skype")

    def test_show_index(self):
        url = reverse('course_interviews:index')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_confirm_interview_without_interview_date(self):
        """
        Student without interview date should not be able to acces confirm_interview page
        """
        url = reverse('course_interviews:confirm_interview', args=(self.student1.uuid, ))
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 404)

    def test_has_confirmed_interview_date_after_confirming_interview(self):
        """
        After confirming the interview, the student should have has_confirmed_interview = True
        """
        self.student1.has_interview_date = True
        self.student1.save()
        url = reverse('course_interviews:confirm_interview', args=(self.student1.uuid, ))
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.get(id=self.student1.id).has_confirmed_interview, True)

    def test_choose_interview_for_student_with_confirmed_interview(self):
        """
        Student with confirmed interview should not be able to select another interview
        """
        self.student1.has_confirmed_interview = True
        self.student1.save()
        url = reverse('course_interviews:choose_interview', args=(self.student1.uuid, ))
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 404)

    def test_choose_interview_slot(self):
        """
        After choosing new interview, student.has_interview_date should be True
        Student in the interview slot should be the right one
        """
        url = reverse('course_interviews:confirm_slot')
        data = {
            "slot_id": self.interview_slot1.id,
            "student_uuid": self.student1.uuid
        }
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.get(id=self.student1.id).has_interview_date, True)
        self.assertEqual(
            InterviewSlot.objects.get(id=self.interview_slot1.id).student, self.student1)

    def test_choose_interview_slot_if_slot_is_already_taken(self):
        """
        Student should't be able to choose a slot that's already taken
        Slots are refreshed every 10 seconds
        If already selected slot is chosen, the student will be promped to choose another interview
        """
        self.interview_slot1.student = self.student2
        self.interview_slot1.save()
        url = reverse('course_interviews:confirm_slot')
        data = {
            "slot_id": self.interview_slot1.id,
            "student_uuid": self.student1.uuid
        }
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 404)

    def test_choose_interview_for_student_with_interview_date(self):
        """
        If the student didn't confirm his interview, he can choose another one
        If he chooses free slot, his previous (autogenerated) slot should become free
        """
        self.interview_slot1.student = self.student1
        self.interview_slot1.save()
        self.student1.has_interview_date = True
        self.student1.save()
        url = reverse('course_interviews:confirm_slot')
        data = {
            "slot_id": self.interview_slot2.id,
            "student_uuid": self.student1.uuid
        }
        self.client.post(url, data, follow=True)

        self.assertEqual(
            InterviewSlot.objects.get(id=self.interview_slot1.id).student, None)
        self.assertEqual(
            InterviewSlot.objects.get(id=self.interview_slot2.id).student, self.student1)
