from course_interviews.models import Student, Teacher, InterviewerFreeTime, InterviewSlot
from course_interviews.helpers.generate_interview_slots import GenerateInterviewSlots
from course_interviews.helpers.generate_interviews import GenerateInterviews
from course_interviews.helpers.generate_emails import GenerateConfirmEmails
from post_office.models import EmailTemplate, Email
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from datetime import date, timedelta


class ManagePyGenerateSlotsTests(TestCase):

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

        self.tomorrow = date.today() + timedelta(days=1)

        self.teacher_free_time1 = InterviewerFreeTime.objects.create(
            teacher=self.teacher_user1,
            date=str(self.tomorrow),
            start_time="15:00",
            end_time="16:00")

        self.teacher_free_time2 = InterviewerFreeTime.objects.create(
            teacher=self.teacher_user2,
            date=str(self.tomorrow),
            start_time="16:00",
            end_time="17:00")

        self.interview_slot1 = InterviewSlot.objects.create(
            teacher_time_slot=self.teacher_free_time1,
            start_time="15:00")

        self.interview_slot2 = InterviewSlot.objects.create(
            teacher_time_slot=self.teacher_free_time2,
            start_time="16:00")

    def test_generate_slots_for_interviewer_free_time_without_generated_slots(self):
        self.test_teacher_user = Teacher.objects.create_user(
            "testuser@user.com", "123", skype="testuser_user")

        self.test_teacher_user.first_name = "Test"
        self.test_teacher_user.last_name = "Testov"
        self.test_teacher_user.is_staff = True
        self.test_teacher_user.groups.add(self.teacher_group)
        self.test_teacher_user.save()

        InterviewerFreeTime.objects.create(
            teacher=self.test_teacher_user,
            date=str(self.tomorrow),
            start_time="15:00",
            end_time="17:00")

        interview_length = 30
        break_between_interviews = 10

        interview_slots_generator = GenerateInterviewSlots(
            interview_length, break_between_interviews)

        # For a total duration of 2 hours and interview_length + break = 40 minutes
        # a total of three interview slots should be generated
        interview_slots_generator.generate_interview_slots()

        client = Client()
        client.login(
            email=self.test_teacher_user.email,
            password='123'
        )

        url = reverse('admin:course_interviews_interviewslot_changelist')
        response = client.get(url, follow=True)

        result_list = response.context_data['cl'].result_list

        # The new teacher should see his three newly generated slots
        self.assertEqual(len(result_list), 3)

    def test_generate_slots_for_interviewer_free_time_with_generated_slots(self):
        """
        No interview slots should be generated, if the interviewer
        free time already has existing slots generated for that period
        """
        client = Client()
        client.login(
            email=self.teacher_admin.email,
            password='123'
        )
        url = reverse('admin:course_interviews_interviewslot_changelist')
        response = client.get(url, follow=True)

        result_list_before_slot_generation = response.context_data['cl'].result_list

        interview_length = 30
        break_between_interviews = 10
        interview_slots_generator = GenerateInterviewSlots(
            interview_length, break_between_interviews)
        interview_slots_generator.generate_interview_slots()

        response = client.get(url, follow=True)
        result_list_after_slot_generation = response.context_data['cl'].result_list

        self.assertCountEqual(result_list_before_slot_generation, result_list_after_slot_generation)


class ManagePyGenerateInterviewsTests(TestCase):

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

        self.student1 = Student.objects.create(
            name="Student One",
            email="student1@student.com",
            skype="student_one_skype")

        self.student2 = Student.objects.create(
            name="Student Two",
            email="student2@student.com",
            skype="student_two_skype")

        self.student3 = Student.objects.create(
            name="Student Three",
            email="student3@student.com",
            skype="student_three_skype")

    def test_generate_interviews_for_students_without_interview_date(self):
        # Create valid time slot
        tomorrow = date.today() + timedelta(days=1)
        InterviewerFreeTime.objects.create(
            teacher=self.teacher_user1,
            date=str(tomorrow),
            start_time="15:00",
            end_time="16:00")

        interview_length = 20
        break_between_interviews = 10

        interview_slots_generator = GenerateInterviewSlots(
            interview_length, break_between_interviews)
        interview_slots_generator.generate_interview_slots()

        interview_generator = GenerateInterviews()
        interview_generator.generate_interviews()
        client = Client()
        client.login(
            email=self.teacher_admin.email,
            password='123'
        )

        # There are only two slots, so only the first two students should have interview dates
        self.assertEqual(Student.objects.get(id=self.student1.id).has_interview_date, True)
        self.assertEqual(Student.objects.get(id=self.student2.id).has_interview_date, True)
        self.assertEqual(Student.objects.get(id=self.student3.id).has_interview_date, False)

    def test_generate_interviews_for_students_with_interview_date(self):
        """
        If a student has interview slot, he should not receive another one
        He can change his slot only through the choose-interview url
        """
        # Create valid time slot
        tomorrow = date.today() + timedelta(days=1)
        InterviewerFreeTime.objects.create(
            teacher=self.teacher_user1,
            date=str(tomorrow),
            start_time="15:00",
            end_time="16:00")

        interview_length = 20
        break_between_interviews = 10

        interview_slots_generator = GenerateInterviewSlots(
            interview_length, break_between_interviews)
        interview_slots_generator.generate_interview_slots()

        self.student1.has_interview_date = True
        self.student1.save()

        interview_generator = GenerateInterviews()
        interview_generator.generate_interviews()
        client = Client()
        client.login(
            email=self.teacher_admin.email,
            password='123'
        )

        # With two slots available and student1 with interview date,
        # all three students should have interview dates
        self.assertEqual(Student.objects.get(id=self.student1.id).has_interview_date, True)
        self.assertEqual(Student.objects.get(id=self.student2.id).has_interview_date, True)
        self.assertEqual(Student.objects.get(id=self.student3.id).has_interview_date, True)

    def test_generate_interview_for_slot_date_before_today(self):
        """
        Interviews for slots with date < today should not be generated
        """
        # Create outdated time slot
        yesterday = date.today() - timedelta(days=1)
        InterviewerFreeTime.objects.create(
            teacher=self.teacher_user1,
            date=str(yesterday),
            start_time="15:00",
            end_time="15:30")

        # Create valid time slot
        tomorrow = date.today() + timedelta(days=1)
        InterviewerFreeTime.objects.create(
            teacher=self.teacher_user1,
            date=str(tomorrow),
            start_time="15:00",
            end_time="15:30")

        interview_length = 20
        break_between_interviews = 10

        interview_slots_generator = GenerateInterviewSlots(
            interview_length, break_between_interviews)
        interview_slots_generator.generate_interview_slots()

        interview_generator = GenerateInterviews()
        interview_generator.generate_interviews()

        yesterday_slot = InterviewSlot.objects.all().filter(teacher_time_slot__date=yesterday)
        yesterday_slot = yesterday_slot[0]

        tomorrow_slot = InterviewSlot.objects.all().filter(teacher_time_slot__date=tomorrow)
        tomorrow_slot = tomorrow_slot[0]

        self.assertEqual(yesterday_slot.student, None)
        self.assertEqual(tomorrow_slot.student, self.student1)


class ManagePyGenerateEmailsTests(TestCase):

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

        self.tomorrow = date.today() + timedelta(days=1)

        self.teacher_free_time1 = InterviewerFreeTime.objects.create(
            teacher=self.teacher_user1,
            date=str(self.tomorrow),
            start_time="15:00",
            end_time="16:00")

        self.teacher_free_time2 = InterviewerFreeTime.objects.create(
            teacher=self.teacher_user2,
            date=str(self.tomorrow),
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

        self.email_confirmation_template = EmailTemplate.objects.create(
            name='test_template',
            subject='Morning, Rado',
            content='Hi, how are you feeling today?',
            html_content='Hi, how are you feeling today?',
        )

    def test_generate_confirmational_email_for_student_with_interview(self):
        """
        Students without interview date should not receive email
        Students that already received confirmational email
        should not receive another one
        """
        self.interview_slot1.student = self.student1
        self.interview_slot1.save()
        self.student1.has_interview_date = True
        self.student1.save()

        template = self.email_confirmation_template.name
        confirm_interview_url = "confirm-interview-test-url"
        choose_interview_url = "choose-interview-test-url"

        confirm_email_generator = GenerateConfirmEmails(
            template, confirm_interview_url, choose_interview_url)

        confirm_email_generator.generate_confirmation_emails()

        client = Client()
        client.login(
            email=self.teacher_admin.email,
            password='123'
        )

        url = reverse('admin:post_office_email_changelist')
        response = client.get(url, follow=True)

        result_list = response.context_data['cl'].result_list

        # Only email for self.student1 should be in Email change list
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0].to[0], self.student1.email)

    def test_generate_confirmational_email_for_student_without_interview(self):
        """
        Students without interview date should not receive email
        """
        template = self.email_confirmation_template.name
        confirm_interview_url = "confirm-interview-test-url"
        choose_interview_url = "choose-interview-test-url"

        confirm_email_generator = GenerateConfirmEmails(
            template, confirm_interview_url, choose_interview_url)

        confirm_email_generator.generate_confirmation_emails()

        client = Client()
        client.login(
            email=self.teacher_admin.email,
            password='123'
        )

        url = reverse('admin:post_office_email_changelist')
        response = client.get(url, follow=True)

        result_list = response.context_data['cl'].result_list

        # All three students dont have interviews
        # There should be no emails generated in Email change list
        self.assertEqual(len(result_list), 0)

    def test_generate_confirmational_email_for_student_that_already_received_email(self):
        """
        Students that already received confirmational email
        should not receive another one
        """
        self.student2.has_received_email = True
        self.student2.save()

        template = self.email_confirmation_template.name
        confirm_interview_url = "confirm-interview-test-url"
        choose_interview_url = "choose-interview-test-url"

        confirm_email_generator = GenerateConfirmEmails(
            template, confirm_interview_url, choose_interview_url)

        confirm_email_generator.generate_confirmation_emails()

        client = Client()
        client.login(
            email=self.teacher_admin.email,
            password='123'
        )

        url = reverse('admin:post_office_email_changelist')
        response = client.get(url, follow=True)

        result_list = response.context_data['cl'].result_list

        # Two students dont have interviews and the third already received email
        # There should be no emails generated in Email change list
        self.assertEqual(len(result_list), 0)
