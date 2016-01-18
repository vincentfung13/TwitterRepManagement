from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse


# Create your views here.
class Register(View):
    def get(self, request):
        return HttpResponse('Registration page')

    def post(self, request):
        pass


class Login(View):
    def get(self, request):
        return HttpResponse('Login page')

    def post(self, request):
        pass


class Logout(View):
    def get(self, request):
        return HttpResponse('Logout view')


class AddEntity(View):
    def get(self, request):
        return HttpResponse('Add entity view')

    def post(self, request):
        pass


# Index page for each user (showing the clickable entity list they are interested in)
class Index(View):
    def get(self, request, username):
        return HttpResponse('Index page for %s' % username)
