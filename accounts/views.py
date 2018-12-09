import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

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
