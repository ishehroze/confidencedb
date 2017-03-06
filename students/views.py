from datetime import date
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.db.models import F
from .models import Student


class BaseView(View):
    template_name = "students/jumbotron.html"

    def get_context_data(self, **kwargs):
        context = {
            "count_overdue": Student.objects.filter(due_date__lt=date.today())
                                    .exclude(amount_paid=F('amount_total'))
                                    .exclude(expiration_date__lt=date.today()
                                             ).count(),
            "count_expired": Student.objects.filter(
                expiration_date__lt=date.today()).count(),
        }

        return context


class StudentView(BaseView):
    template_name = "students/demo/details.html"

    def get_context_data(self, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)

        roll = kwargs["roll"]
        context["student"] = Student.objects.get(roll=roll)
        return context

    def get(self, request, **kwargs):
        try:
            return render(request, self.template_name,
                          self.get_context_data(**kwargs))
        except Student.DoesNotExist:
            template_name = "students/demo/student_does_not_exist.html"
            context = {"roll": kwargs["roll"]}
            return render(request, template_name, context)


class AttendancesView(StudentView):
    template_name = "students/demo/attendances.html"


class TestsView(StudentView):
    template_name = "students/demo/tests.html"


class SheetsView(StudentView):
    template_name = "students/demo/sheets.html"


class GetStudentView(StudentView):
    def get(self, request, **kwargs):
        if request.GET.get('roll'):
            roll = request.GET.get('roll')
            return HttpResponseRedirect(
                reverse_lazy('students:details', args=[roll]))
        else:
            return HttpResponseRedirect(
                reverse_lazy('index'))
