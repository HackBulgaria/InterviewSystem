from django.conf.urls import url

from .views import index, get_students, get_emails, confirm_interview, choose_interview, confirm_slot, get_interview_slots

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^api/get-students/(?P<course>[-\w]+)/$', get_students, name="get_students"),
    url(r'^api/get-emails/$', get_emails, name="get_emails"),
    url(r'^api/get-interview-slots/$', get_interview_slots, name="get_interview_slots"),
    url(r'^confirm-interview/(?P<token>[-\w]+)/$', confirm_interview, name="confirm_interview"),
    url(r'^choose-interview/(?P<token>[-\w]+)/$', choose_interview, name="choose_interview"),
    url(r'^confirm-slot/$', confirm_slot, name="confirm_slot"),
]
