from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Visit, UserInOlimp


@login_required
def people_inside(request):
    users = UserInOlimp.objects.inside_now()
    return render(request, 'visits/index.html', context={'users': users})


@login_required
def open(request):
    current_user = request.user

    try:
        # Проверка наличия "незавершенного посещения"
        latest_visit = Visit.objects\
            .filter(user=current_user, enter_timestamp__isnull=True)\
            .latest('enter_timestamp')
        latest_visit.enter_timestamp = timezone.now()
        latest_visit.save(update_fields=['enter_timestamp'])
    except Visit.DoesNotExist:
        Visit.objects.create(user=request.user, enter_timestamp=timezone.now())

    return redirect("visits:people_inside")


@login_required
def close(request):
    _error = ''
    current_user = request.user

    try:
        # Проверка наличия "незавершенного посещения"
        latest_visit = Visit.objects \
            .filter(user=current_user, leave_timestamp__isnull=True) \
            .latest('enter_timestamp')
        latest_visit.leave_timestamp = timezone.now()
        latest_visit.save(update_fields=['leave_timestamp'])
    except Visit.DoesNotExist:
        _error = "Данные о вашем входе не найдены."
    return redirect("visits:people_inside")


def status(request):
    count_user = UserInOlimp.objects.inside_now().exists()
    return render(request, 'visits/status.html', context={'flag': bool(count_user)})