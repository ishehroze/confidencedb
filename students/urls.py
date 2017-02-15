from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^000000/$', TemplateView.as_view(
        template_name="students/demo/details.html"
    ), name='demo_details'),
    url(r'^000000/attendances/$', TemplateView.as_view(
        template_name="students/demo/attendances.html"
    ), name='demo_attendences'),
    url(r'^000000/tests/$', TemplateView.as_view(
        template_name="students/demo/tests.html"
    ), name='demo_tests'),
    url(r'^000000/sheets/$', TemplateView.as_view(
        template_name="students/demo/sheets.html"
    ), name='demo_sheets'),
]
