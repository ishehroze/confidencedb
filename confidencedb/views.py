from django.shortcuts import render
from students.views import BaseView


class IndexView(BaseView):
    template_name = "students/jumbotron.html"

    def get(self, request):
        return render(request, self.template_name, 
                      self.get_context_data())
