from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from .forms import RegisterForm


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())
