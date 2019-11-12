import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import DetailView
from .models import ServiceDocument
from .utils import *


def reg(request):
    return render(request, 'registration.html')

# class RegistrationUser(ObjectRegistrUserMixin, View)

# next_page = request.GET['next']
# if request.user.is_authenticated():
#     return HttpResponseRedirect(next_page)
# else:
#     if request.method == 'POST':
#         if form.is_valid:
#             username = form.cleaned_data('username')


class PrintPage(DetailView):
    queryset = ServiceDocument.objects.all()
    template_name = 'documents/over_time.html'
