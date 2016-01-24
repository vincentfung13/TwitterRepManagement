from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponseRedirect


class MainPage(View):
    def get(self, request):
        if request.user.is_authenticated():
            # Redirect to user index page
            return HttpResponseRedirect('/user_handle/%s/' % request.user.username)
        else:
            # display home page main content
            context = {}
            return render(request, 'main.html', context)
