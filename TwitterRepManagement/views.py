from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class MainPage(View):
    def get(self, request):
        if request.user.is_authenticated():
            # Redirect to user index page
            return HttpResponseRedirect(reverse('user_handle:Index'))
        else:
            # display home page main content
            context = {}
            return render(request, 'main.html', context)
