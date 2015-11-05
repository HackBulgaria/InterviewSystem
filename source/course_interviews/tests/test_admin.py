from course_interviews.models import Student, Teacher, InterviewerFreeTime, InterviewSlot
from course_interviews.helpers.generate_interview_slots import GenerateInterviewSlots
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from datetime import date, timedelta


class AdminPanelTests(TestCase):

    def setUp(self):
        self.teacher_admin = Teacher.objects.create_superuser(
            "admin@admin.com", "123", skype="admin_hackbulgaria")

        self.teacher_user1 = Teacher.objects.create_user(
            "user1@user.com", "123", skype="user1_user")

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

        self.tomorrow = date.today() + timedelta(days=1)

        self.teacher_free_time1 = InterviewerFreeTime.objects.create(
            teacher=self.teacher_user1,
            date=str(self.tomorrow),
            start_time="15:00",
            end_time="16:00")

        self.interview_slot1 = InterviewSlot.objects.create(
            teacher_time_slot=self.teacher_free_time1,
            start_time="15:00")

        self.student1 = Student.objects.create(
            name="Student One",
            email="student1@student.com",
            skype="student_one_skype")

    def test_interviewer_free_time_admin_queryset_for_teacher_user(self):
        """
        teacher_user should see only his interview free times
        """
        client = Client()
        client.login(
            email=self.teacher_user1.email,
            password='123'
        )
        url = reverse('admin:course_interviews_interviewerfreetime_changelist')
        response = client.get(url, follow=True)
        result_list = response.context_data['cl'].result_list
        change_list = self.teacher_user1.interviewerfreetime_set.all()

        self.assertCountEqual(change_list, result_list)

    def test_interviewer_free_time_admin_save_model_on_create(self):
        """
        save_model should put teacher_user on create object
        """
        client = Client()
        client.login(
            email=self.teacher_user1.email,
            password='123'
        )

        data = {
            'date': str(self.tomorrow),
            'start_time': '18:00',
            'end_time': '19:00'
        }
        url = reverse('admin:course_interviews_interviewerfreetime_add')
        client.post(url, data, follow=True)
        new_teacher_free_time = InterviewerFreeTime.objects.latest('id')

        self.assertEqual(new_teacher_free_time.teacher, self.teacher_user1)

    def test_interview_slot_admin_change_for_teacher_user(self):
        """
        teacher_user should be able to see the slots (has change permissions),
        but should not be able to edit the slots (Forbidden - Error 403)
        """
        client = Client()
        client.login(
            email=self.teacher_user1.email,
            password='123'
        )
        url = reverse(
            'admin:course_interviews_interviewslot_change',
            args=(self.interview_slot1.id, ))
        data = {
            "student": self.student1
        }
        response = client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 403)

    def test_interview_slot_admin_queryset_for_teacher_user(self):
        """
        teacher_user should see only his interview slots
        """
        client = Client()
        client.login(
            email=self.teacher_user1.email,
            password='123'
        )
        url = reverse('admin:course_interviews_interviewslot_changelist')
        response = client.get(url, follow=True)
        result_list = response.context_data['cl'].result_list
        change_list = InterviewSlot.objects.all().filter(teacher_time_slot=self.teacher_free_time1)

        self.assertCountEqual(change_list, result_list)

    def test_change_permissions_interviewer_free_time_after_slots_are_generated(self):
        """
        teacher should not be able to delete his interview_free_time if slots
        for that time are already generated - no interviews are gona be unanswered
        if he can not attend some interview, he has to tell us
        """
        test_teacher_user = Teacher.objects.create_user(
            "testuser@user.com", "123", skype="testuser_user")

        test_teacher_user.first_name = "Test"
        test_teacher_user.last_name = "Testov"
        test_teacher_user.is_staff = True
        test_teacher_user.groups.add(self.teacher_group)
        test_teacher_user.save()

        interview_length = 20
        break_between_interviews = 10
        interview_slots_generator = GenerateInterviewSlots(
            interview_length, break_between_interviews)

        time_slot = InterviewerFreeTime.objects.create(
            teacher=test_teacher_user,
            date=str(self.tomorrow),
            start_time="15:00",
            end_time="15:30")

        interview_slots_generator.generate_interview_slots()

        client = Client()
        client.login(
            email=test_teacher_user.email,
            password='123'
        )

        url = reverse('admin:course_interviews_interviewerfreetime_change',
                      args=(time_slot.id, ))

        data = {
            "buffer_time": True
        }

        response = client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 403)
