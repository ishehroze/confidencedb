from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', 
		views.GetStudentView.as_view(), name='get'), 
    url(r'^(?P<roll>[A-Za-z0-9]+)/$', 
    	views.StudentView.as_view(), name='details'),
    url(r'^(?P<roll>[A-Za-z0-9]+)/attendances/$', 
    	views.AttendancesView.as_view(), name='attendences'),
    url(r'^(?P<roll>[A-Za-z0-9]+)/tests/$',
    	views.TestsView.as_view(), name='tests'),
    url(r'^(?P<roll>[A-Za-z0-9]+)/sheets/$',
    	views.SheetsView.as_view(), name='sheets'),
]
