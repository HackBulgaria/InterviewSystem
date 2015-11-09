from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import Student, Teacher, InterviewerFreeTime, InterviewSlot

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.conf.urls import patterns, include, url

from .helpers.generate_interview_slots import GenerateInterviewSlots
from .helpers.generate_interviews import GenerateInterviews
from .helpers.generate_emails import GenerateConfirmEmails, GenerateNewCoursesEmails
from interview_communicator.local_settings import confirm_interview_url, choose_interview_url


class UserCreationForm(forms.ModelForm):

    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Teacher
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('get_full_name', 'email', 'skype')
    list_filter = ('is_admin',)

    ordering = None

    fieldsets = (
        (None, {
            'fields': (
                'email', 'password', 'first_name', 'last_name', 'skype',
                'groups', 'is_active', 'is_staff', 'is_superuser')
            }),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'skype', 'password1', 'password2')
            }),
        )

admin.site.register(Teacher, MyUserAdmin)


class StudentAdmin(admin.ModelAdmin):

    def get_first_task(self, obj):
        return u"<a href='{0}' target='_blank'>link</a>".format(obj.first_task)
    get_first_task.allow_tags = True
    get_first_task.short_description = "First task"
    get_first_task.admin_order_field = 'first_task'

    def get_second_task(self, obj):
        return u"<a href='{0}' target='_blank'>link</a>".format(obj.second_task)
    get_second_task.allow_tags = True
    get_second_task.short_description = "Second task"
    get_second_task.admin_order_field = 'second_task'

    def get_third_task(self, obj):
        return u"<a href='{0}' target='_blank'>link</a>".format(obj.third_task)
    get_third_task.allow_tags = True
    get_third_task.short_description = "Third task"
    get_third_task.admin_order_field = 'third_task'

    list_display = [
        'name',
        'email',
        'skype',
        'phone_number',
        'applied_course',
        'get_first_task',
        'get_second_task',
        'get_third_task',
        'code_skills_rating',
        'code_design_rating',
        'fit_attitude_rating',
        'has_interview_date',
        'has_confirmed_interview',
        'has_been_interviewed',
        'is_accepted'
    ]
    list_filter = [
        'applied_course',
        'code_skills_rating',
        'code_design_rating',
        'fit_attitude_rating',
        'has_confirmed_interview',
        'has_been_interviewed',
        'is_accepted'
    ]
    search_fields = ['name', 'email', 'skype']
    readonly_fields = ('uuid',)

admin.site.register(Student, StudentAdmin)


class InterviewerFreeTimeAdmin(admin.ModelAdmin):
    model = InterviewerFreeTime

    def has_change_permission(self, request, obj=None):
        if obj and request.POST and not request.user.is_superuser and obj.has_generated_slots():
            return False
        return super().has_change_permission(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude = ['teacher', 'buffer_time']
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change and not request.user.is_superuser:
            obj.teacher = request.user
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(teacher=request.user)

    def get_generated_slots(self, obj):
        return obj.has_generated_slots()
    get_generated_slots.short_description = "Has generated slots"
    get_generated_slots.boolean = True

    list_display = [
        "teacher",
        "date",
        "start_time",
        "end_time",
        'get_generated_slots'
    ]
    list_filter = ["date", "start_time", "end_time"]
    search_fields = ["teacher"]
    ordering = ['date', 'start_time']

admin.site.register(InterviewerFreeTime, InterviewerFreeTimeAdmin)


class InterviewSlotAdmin(admin.ModelAdmin):

    # Generate interview slots using the free time of the teachers(interviewers)

    def generate_slots(self, request):
        if request.user.is_superuser:
            interview_length = 20
            break_between_interviews = 10

            interview_slots_generator = GenerateInterviewSlots(
                interview_length, break_between_interviews)

            interview_slots_generator.generate_interview_slots()
            generated_slots = interview_slots_generator.get_generated_slots()

            self.message_user(
                request, "%s slots were generated"
                % generated_slots)

            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:
            return HttpResponseForbidden()

    # Generate interviews using the free slots and the students without interviews
    def generate_interviews(self, request):
        if request.user.is_superuser:
            interview_generator = GenerateInterviews()
            interview_generator.generate_interviews()

            generated_interviews = interview_generator.get_generated_interviews_count()
            students_without_interviews = interview_generator.get_students_without_interviews()

            self.message_user(
                request, "%s interviews were generated"
                % generated_interviews)
            self.message_user(
                request, "%s students do not have interview date"
                % students_without_interviews)

            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:
            return HttpResponseForbidden()

    # Generate emails for interview date confirmation
    def generate_emails(self, request):
        if request.user.is_superuser:
            # Generate emails for the new courses
            # template = 'new_courses'
            # email_generator = GenerateNewCoursesEmails(template)
            # email_generator.generate_new_courses_emails()

            template = 'interview_confirmation'

            email_generator = GenerateConfirmEmails(
                template, confirm_interview_url, choose_interview_url)

            email_generator.generate_confirmation_emails()

            generated_emails = email_generator.get_generated_emails()
            students_with_emails = email_generator.get_students_with_generated_emails()
            students_without_emails = email_generator.get_students_without_generated_emails()

            self.message_user(
                request, "%s  confirmational emails were generated"
                % generated_emails)
            self.message_user(
                request, "There are %s students with generated confirmational emails"
                % students_with_emails)
            self.message_user(
                request, "%s students still do NOT have confirmational emails"
                % students_without_emails)
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:
            return HttpResponseForbidden()

    def get_urls(self):
        urls = super().get_urls()
        my_urls = patterns(
            "",
            url(r"^generate_slots/$", self.generate_slots, name="generate_slots"),
            url(r"^generate_interviews/$", self.generate_interviews, name="generate_interviews"),
            url(r"^generate_emails/$", self.generate_emails, name="generate_emails")
        )
        return my_urls + urls

    def has_change_permission(self, request, obj=None):
        if obj and request.POST and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(
            teacher_time_slot=request.user.interviewerfreetime_set.all())

    def get_date(self, obj):
        return obj.teacher_time_slot.date
    get_date.short_description = 'Date'
    get_date.admin_order_field = 'teacher_time_slot__date'

    def get_start_time(self, obj):
        return obj.start_time
    get_start_time.short_description = "Starting"
    get_start_time.admin_order_field = "start_time"

    def get_student(self, obj):
        if obj.student_id and obj.student.name:
            return u"<a href='../student/{0}/'>{1}</a>".format(obj.student_id, obj.student.name)
        return
    get_student.short_description = "Student"
    get_student.allow_tags = True

    def get_teacher(self, obj):
        return obj.teacher_time_slot.teacher
    get_teacher.short_description = "Teacher"

    def get_student_confirmation(self, obj):
        if obj.student_id:
            return obj.student.has_confirmed_interview
        return
    get_student_confirmation.short_description = "Confirmed interview"
    get_student_confirmation.boolean = True

    def get_student_has_been_interviewed(self, obj):
        if obj.student_id:
            return obj.student.has_been_interviewed
        return
    get_student_has_been_interviewed.short_description = "Has been interviewed"
    get_student_has_been_interviewed.boolean = True

    def get_teacher_skype(self, obj):
        return obj.teacher_time_slot.teacher.skype
    get_teacher_skype.short_description = "Teacher Skype"

    def get_student_skype(self, obj):
        if obj.student_id:
            return obj.student.skype
        return
    get_student_skype.short_description = "Student Skype"

    def get_student_course(self, obj):
        if obj.student_id:
            return obj.student.applied_course
        return
    get_student_course.short_description = "Applying for"

    list_display = [
        'get_date',
        'get_start_time',
        'get_student',
        'get_student_skype',
        'get_teacher',
        'get_teacher_skype',
        'get_student_course',
        'get_student_confirmation',
        'get_student_has_been_interviewed',
    ]
    ordering = ['teacher_time_slot__date', 'start_time']

admin.site.register(InterviewSlot, InterviewSlotAdmin)
