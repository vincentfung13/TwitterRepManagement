from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user
from user_handle.models import UserEntity


class MainPage(View):
    def get(self, request):
        if request.user.is_authenticated():
            # Redirect to user index page
            return HttpResponseRedirect(reverse('user_handle:Index'))
        else:
            # display home page main content
            context = {}
            return render(request, 'main.html', context)


class About(View):
    def get(self, request):
        context = {}
        user = get_user(request)
        if user.is_authenticated():
            interest_list = [ue_orm.entity for ue_orm in UserEntity.objects.filter(user=user)]
            context = {
                'interest_list': interest_list,
            }
        return render(request, 'about.html', context)