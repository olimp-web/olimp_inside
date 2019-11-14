import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from .forms import FormRegister


def reg(request):
    return render(request, 'registration.html')


class RegistrationFormView(FormView):
    form_class = FormRegister
    success_url = '/gates/'
    template_name = 'registration.html'

    def form_valid(self, form):
        form.save()
        return super(RegistrationFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegistrationFormView, self).form_invalid(form)

# class RegistrationUser(ObjectRegistrUserMixin, View)

# next_page = request.GET['next']
# if request.user.is_authenticated():
#     return HttpResponseRedirect(next_page)
# else:
#     if request.method == 'POST':
#         if form.is_valid:
#             username = form.cleaned_data('username')
