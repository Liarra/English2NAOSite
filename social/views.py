from django.http import HttpResponse
from django.shortcuts import render
from translator.models import Scenario

__author__ = 'NBUCHINA'


def main_page(request):
    our_user = request.user
    user_library = []
    user_scenarios = Scenario.objects.filter(user=our_user.id)

    context = {'user': our_user, 'library': user_library, 'scenarios': user_scenarios}
    return render(request, "site_base.html", context)

