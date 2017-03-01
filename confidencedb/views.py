from django.shortcuts import render
from django.views import View
from students.models import Student
from students.views import BaseView

class IndexView(BaseView):
    template_name = "students/jumbotron.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name, 
            self.get_context_data())