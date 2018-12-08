import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .utils import *

from .models import UserInOlimp, UserAccount, models


@login_required
def peopleInside(request):
    # users = UserInOlimp.objects.all()
    users = UserAccount.objects.filter(in_olimp=True)
    # .select_related('UserInOlimp')
    # users = UserAccount.objects.filter(entrance_to_olimp=timezone.now()).select_related('UserInOlimp')
    # print(dict(users))
    return render(request, 'index.html', context={'users': users})


def open(request):
    user_in_olimp = request.user
    user_in_olimp.in_olimp = True

    user_in_olimp.save()

    user_id = request.user.id


    try:
        _u = UserInOlimp.objects.filter(user=user_in_olimp).latest('last_visit')
        if _u is not None:
            raise models.ObjectDoesNotExist
        _u.entrance_to_olimp = datetime.datetime.now()
        _u.save(update_fields=['entrance_to_olimp'])

    except models.ObjectDoesNotExist:
        UserInOlimp.objects.create(user=request.user, entrance_to_olimp=datetime.datetime.now())

    users = UserAccount.objects.filter(in_olimp=True)

    return render(request, 'index.html', context={'users': users})


def close(request):
    user_in_olimp = request.user
    user_in_olimp.in_olimp = False

    user_in_olimp.save()

    try:
        _u = UserInOlimp.objects.filter(user=user_in_olimp).latest('entrance_to_olimp')
        _u_exit = UserInOlimp.objects.filter(user=user_in_olimp).latest('last_visit')
        if _u is None or _u_exit is not None:
            raise models.ObjectDoesNotExist
        _u.update.last_visit = datetime.datetime.now()
        _u.save(update_fields=['last_visit'])
        message = False

    except models.ObjectDoesNotExist:
        message = True

    users = UserAccount.objects.filter(in_olimp=True)
        # .prefetch_related('visits')
    return render(request, 'index.html', context={'users': users, 'message':message})


def status(request):
    count_user = UserAccount.objects.filter(in_olimp=True).exists()
    if count_user:
        return render(request, 'status.html', context={'flag': True})
    return render(request, 'status.html', context={'flag': False})


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
