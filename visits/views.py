from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from accounts.models import UserAccount
from .models import Visit

# Create your views here.


@login_required
def people_inside(request):
    users = UserAccount.objects.filter(in_olimp=True)
    return render(request, 'index.html', context={'users': users})


@login_required
def open(request):
    current_user = request.user

    try:
        # Проверка наличия "незавершенного посещения"
        latest_visit = Visit.objects\
            .filter(user=current_user, entrance_to_olimp__isnull=True)\
            .latest('entrance_to_olimp')
        latest_visit.entrance_to_olimp = timezone.now()
        latest_visit.save(update_fields=['entrance_to_olimp'])
    except Visit.DoesNotExist:
        Visit.objects.create(user=request.user, entrance_to_olimp=timezone.now())

    # mark User as indor
    current_user.in_olimp = True
    current_user.save()

    users = UserAccount.objects.filter(in_olimp=True)

    return render(request, 'index.html', context={'users': users})


@login_required
def close(request):
    _error = ''
    current_user = request.user

    try:
        # Проверка наличия "незавершенного посещения"
        latest_visit = Visit.objects \
            .filter(user=current_user, last_visit__isnull=True) \
            .latest('entrance_to_olimp')
        latest_visit.last_visit = timezone.now()
        latest_visit.save(update_fields=['last_visit'])
    except Visit.DoesNotExist:
        _error = "Данные о ващем входе не найдены."
        #
        # _u = Visit.objects.filter(user=user_in_olimp).latest('entrance_to_olimp')
        # _u_exit = Visit.objects.filter(user=user_in_olimp).latest('last_visit')
        # if _u is None or _u_exit is not None:
        #     raise models.ObjectDoesNotExist
        # _u.update.last_visit = datetime.datetime.now()
        # _u.save(update_fields=['last_visit'])
        # message = False

    # except models.ObjectDoesNotExist:
    #     message = True

    users = UserAccount.objects.filter(in_olimp=True)
        # .prefetch_related('visits')
    return render(request, 'index.html', context={'users': users, 'error': _error})


def status(request):
    count_user = UserAccount.objects.filter(in_olimp=True).exists()
    return render(request, 'status.html', context={'flag': bool(count_user)})